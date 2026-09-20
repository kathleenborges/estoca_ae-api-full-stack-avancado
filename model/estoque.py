from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime

from model.base import Base


class Estoque(Base):
    __tablename__ = "estoque"

    id = Column(Integer, primary_key=True)
    quantidade_disponivel = Column(Integer, nullable=False)
    data_entrada = Column(String(20), default=lambda: datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

    solicitacao_id = Column(
        Integer,
        ForeignKey("solicitacao.id"),
        unique=True,
        nullable=False
    )

    solicitacao = relationship("Solicitacao", back_populates="estoque")

    @property
    def cadastro_id(self):
        """Busca o ID do cadastro através do relacionamento com a solicitação"""
        if self.solicitacao:
            return self.solicitacao.cadastro_id
        return None

    @property
    def nome(self):
        """Busca o Nome do produto através da solicitação -> cadastro"""
        if self.solicitacao and self.solicitacao.cadastro:
            return self.solicitacao.cadastro.nome
        return "Material não identificado"
