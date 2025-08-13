from datetime import timedelta

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from auth_conf import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, \
    get_current_user
from database import get_db_session, Usuario
import schemas

# configuração do hash de senhas
app = FastAPI()

@app.get("/") # home page da api para apresentação
def root():
    return {"message": "Bem vindo a API de autenticação feita com kayky azevedo, Use /login, /cadastro, ou /showUser para interagir "}


@app.post("/cadastro") #endpoint de cadastro
def cadastro(user: schemas.UserCreate, db: Session = Depends(get_db_session)):
    try:
        hashed_password = get_password_hash(user.password) # faz o hash
        db_user = Usuario(nome_usuario=user.username,
                          nome_completo=user.full_name,
                          hash_senha=hashed_password,)  # a variavel db_user recebe a classe Usuario
                                                        # que é usada na comunicação com o banco
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
       )

# rota de login
@app.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)):
    # Buscar o usuário no banco de dados
    user = db.query(Usuario).filter(Usuario.nome_usuario == form_data.username).first()

    # Verifica se o usuário existe e se a senha está correta
    if not user or not verify_password(form_data.password, user.hash_senha):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de usuário ou senha incorretos."
        )

    # Geraração do token de acesso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.nome_usuario}, expires_delta=access_token_expires
    )

    # 4. Retornar o token
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/showUser") # Rota protaegida
def show_user(current_user: Usuario = Depends(get_current_user)):
    return {"user_info": current_user}

if __name__ == "__main__":
    uvicorn.run(app, port=8000)