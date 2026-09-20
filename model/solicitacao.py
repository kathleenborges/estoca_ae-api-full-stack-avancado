from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model.base import Base


class Solicitacao(Base):
    __tablename__ = "solicitacao"

    id = Column(Integer, primary_key=True)
    quantidade = Column(Integer, nullable=False)
    data_solicitacao = Column(String(20), default=lambda: datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    data_necessidade = Column(String(20), default=lambda: datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    data_atendimento = Column(String(20), nullable=True)
    status = Column(String(20), default="PENDENTE",nullable=False)
    cadastro_id = Column(Integer, ForeignKey("cadastro.id"), nullable=False)

    # Relacionamento N:1 (muitas solicitações → um cadastro)
    cadastro = relationship("Cadastro", back_populates="solicitacoes")

    # Relacionamento 1:1 com Estoque
    estoque = relationship(
        "Estoque",
        back_populates="solicitacao",
        uselist=False,
        cascade="all, delete-orphan"
    )
    
    @property
    def nome_material(self):
        """Busca o nome do material através do relacionamento com o Cadastro"""
        if self.cadastro:
            return self.cadastro.nome
        return "Material não encontrado"
        
    def __init__(self, quantidade: int, cadastro_id: int, 
                 data_necessidade: Union[str, None] = None,
                 status: str = "PENDENTE"):
        """
        Cria uma nova solicitação
        """
        self.quantidade = quantidade
        self.cadastro_id = cadastro_id
        self.status = status
        
        # Se o front enviar uma data (como "2025-12-31"), usamos ela
        if data_necessidade:
            self.data_necessidade = data_necessidade
