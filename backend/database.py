from sqlalchemy import String, text
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from datetime import datetime
import os

# A base é a classe que os seus modelos vão herdar
Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL")


class Usuario(Base):
    """
    Modelo de dados para a tabela 'usuarios'.
    """
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
        """
        Representação em string do objeto, útil para debug.
        """
        return f"Usuario(id={self.id_usuario}, nome_usuario='{self.nome_usuario}')"