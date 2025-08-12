from sqlalchemy import String, text, create_engine
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# A base é a classe que os seus modelos vão herdar
Base = declarative_base()

DATABASE_URI = os.getenv("DATABASE_URI")

engine = create_engine(DATABASE_URI, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Usuario(Base):

    __tablename__ = 'usuarios'

    # Mapeamento das colunas da sua tabela
    id_usuario: Mapped[int] = mapped_column(primary_key=True)
    nome_completo: Mapped[str] = mapped_column(String(100))
    nome_usuario: Mapped[str] = mapped_column(String(50), unique=True)
    hash_senha: Mapped[str] = mapped_column(String(255))
    setor: Mapped[str | None] = mapped_column(String(50), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP")
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )

    def __repr__(self) -> str:
        return f"Usuario(id={self.id_usuario}, nome_usuario='{self.nome_usuario}')"