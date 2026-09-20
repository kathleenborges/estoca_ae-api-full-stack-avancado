from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """ Representação da mensagem de erro """
    message: str