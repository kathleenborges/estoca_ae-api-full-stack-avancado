from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# importando os elementos definidos no modelo
from model.base import Base
from model.cadastro import Cadastro
from model.estoque import Estoque
from model.solicitacao import Solicitacao


# Database Configuração
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "db.sqlite3")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# cria a engine de conexão com o banco
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
    echo=False
)

# Instancia um criador de seção com o banco
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
