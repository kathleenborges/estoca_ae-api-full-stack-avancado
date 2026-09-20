from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class RespostaEstoqueSchema(BaseModel):
    id: int
    quantidade_disponivel: int
    data_entrada: str
    cadastro_id: Optional[int] = None
    nome: str

    model_config = ConfigDict(from_attributes=True)

class ListaEstoqueSchema(BaseModel):
    """ Define como a lista de itens em estoque será retornada """
    estoque: List[RespostaEstoqueSchema]
    
