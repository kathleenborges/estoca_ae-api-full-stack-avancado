from pydantic import BaseModel


class MensagemSchema(BaseModel):
    """ Resposta simples com uma mensagem de texto """
    message: str = "Operação realizada com sucesso"