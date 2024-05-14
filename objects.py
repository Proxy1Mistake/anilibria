from pydantic import BaseModel

class Login(BaseModel):
    err: str
    mes: str
    key: str
    sessionId: str

class Catalog(BaseModel):
    err: str
    table: str
    total: int
    update: str