from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model.base import Base


class Cadastro(Base):
    __tablename__ = 'cadastro'

    id = Column(Integer, primary_key=True)
    nome = Column(String(140), unique=True, nullable=False)
    valor = Column(Float, nullable=False)
    link = Column(String(400), unique=True, nullable=False)
    data_cadastro = Column(String(20), default=lambda: datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

    # Relacionamento 1:N com Solicitação
    solicitacoes = relationship(
        "Solicitacao",
        back_populates="cadastro",
        cascade="all, delete-orphan"
    )

    def __init__(self, nome:str, valor:float, link:str,
                 data_cadastro: Union[str, None] = None):
        """
        Cadastrando o material

        Arguments:
            nome: nome do material.
            valor: valor do site para o material
            link: link onde se encontra para comprar aquele material
            data_cadastro: data de quando o material foi cadastrado na base
        """
        self.nome = nome
        self.valor = valor
        self.link = link

        # se não for informada, será o data exata da inserção no banco
        if data_cadastro:
            self.data_cadastro = data_cadastro

    def adiciona_solicitacao(self, solicitacao: "Solicitacao"):
        """ Faz uma solicitacao do material
        """
        self.solicitacoes.append(solicitacao)

