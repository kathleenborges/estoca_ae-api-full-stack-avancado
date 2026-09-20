from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Literal 
from schemas.estoque import RespostaEstoqueSchema

class CriacaoSolicitacaoSchema(BaseModel):
    cadastro_id: int = 2
    data_necessidade: str = Field(default="2026-01-29T00:00:00")
    quantidade: int = 1

    model_config = ConfigDict(
        
        json_schema_extra={
            "example": {
                "cadastro_id": 2,
                "data_necessidade": "2026-01-29T00:00:00",
                "quantidade": 1
            }
        }
    )

class SolicitacaoUpdateStatusSchema(BaseModel):
    status: Literal["PENDENTE", "ATENDIDA"]

class RespostaSolicitacaoSchema(BaseModel):
    id: int
    quantidade: int
    status: str
    nome_material: str
    data_solicitacao: str
    data_necessidade: Optional[str] = "2026-01-29T00:00:00"
    data_atendimento: Optional[str] = "2026-01-29T00:00:00"
    estoque: Optional[RespostaEstoqueSchema] 

    model_config = ConfigDict(from_attributes=True)

class ListaSolicitacoesSchema(BaseModel):
    """ Define como a lista de solicitações será retornada """
    solicitacoes: List[RespostaSolicitacaoSchema]
