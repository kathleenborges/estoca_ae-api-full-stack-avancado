from pydantic import BaseModel


class IdPathSchema(BaseModel):
    id: int
