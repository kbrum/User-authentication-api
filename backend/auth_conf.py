from datetime import datetime, timezone, timedelta

from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import os

from sqlalchemy.orm import Session
from starlette import status

from backend.database import get_db_session, Usuario

# configuração do hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# configuração do token JWT
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# função que faz o hash das senhas
def get_password_hash(password) -> str:
    return pwd_context.hash(password)

# função que faz a verificação da senha para login
def verify_password(text_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(text_password, hashed_password)

# função usada para criar o token web
def create_access_token(data: dict, expires_delta: timedelta | None = None):

    # Copia os dados necessarios
    to_encode = data.copy()

    # Define a data de expiração do token
    if expires_delta:
        # Se um tempo de expiração for fornecido (ex: 30 minutos),
        # ele é adicionado ao tempo atual.
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Se nenhum tempo for fornecido, a expiração padrão é 15 minutos.
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    # Adiciona a data de expiração aos dados
    to_encode.update({"exp": expire})

    # Codifica o token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Retorna o token codificado
    return encoded_jwt

def get_current_user(db: Session = Depends(get_db_session), token: str = Depends(oauth2_scheme)):
    try:
        # Decodifica o token usando a chave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Extrai o nome de usuário do payload do token
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

        # Busca o usuário no banco de dados
    user = db.query(Usuario).filter(Usuario.nome_usuario == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")

    return user