from backend.database import get_db_session, Usuario
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
import schemas
import uvicorn

# confi guração do hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()

# função que faz o hash das senhas
def get_password_hash(password):
    return pwd_context.hash(password)

@app.get("/home")
def root():
    return {"message": "Bem vindo a API de autenticação feita com kayky azevedo, Use /login, /cadastro, ou /showUser para interagir "}


@app.get("/cadastro")
def cadastro(user: schemas.UserCreate, db: Session = Depends(get_db_session)):
    try:
        hashed_password = get_password_hash(user.password)
        db_user = Usuario(nome_usuario=user.username,
                          nome_completo=user.full_name,
                          hash_senha=hashed_password,)
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


if __name__ == "__main__":
    uvicorn.run(app, port=8000)