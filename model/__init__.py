from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
import os

from model.base import Base
from model.cadastro import Cadastro
from model.estoque import Estoque
from model.solicitacao import Solicitacao

# Database Configuração
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "db.sqlite3")

# Permite trocar o banco (ex.: nos testes) sem mexer no código
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool if ":memory:" in DATABASE_URL else None,
    echo=False
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)