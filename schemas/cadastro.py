from pydantic import BaseModel, ConfigDict 
from typing import List

class CriacaoCadastroSchema(BaseModel):
    """ Define como um novo cadastro deve ser enviado """
    nome: str = "Sapato"
    valor: float = 100.00
    link: str = "https://www.google.com"


class RespostaCadastroSchema(BaseModel):
    """ Define como os dados do cadastro serão retornados """
    id: int 
    nome: str = "Sapato"
    valor: float = 100.00
    link: str = "https://www.google.com"
    data_cadastro: str 

    model_config = ConfigDict(from_attributes=True)

class ListaCadastrosSchema(BaseModel):
    """ Define como uma lista de cadastros será retornada.
    """
    cadastros: List[RespostaCadastroSchema]

class CadastroBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    nome: str = "Sapato"

class CadastroDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    nome: str
