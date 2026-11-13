from typing import List, Optional
from pydantic import BaseModel, EmailStr

from schemas.artigo_schema import ArtigoSchema

class UsuarioSchema(BaseModel):
    id: Optional[int]
    nome: str
    email: EmailStr
    eh_admin: bool = False

    class Config:
        orm_mode = True

class UsuarioSchemaBase(BaseModel):
    senha: str


class UsuarioSchemaRead(BaseModel):
    id: int
    nome: str
    sobrenome: str
    email: EmailStr
    eh_adm: Optional[bool] = None
    ativo: Optional[bool] = None

    class Config:
        from_attributes = True


class UsuarioSchemaCreate(UsuarioSchemaBase):
    nome: str
    sobrenome: str
    email: EmailStr


class UsuarioSchemaArtigos(UsuarioSchemaRead):
    artigos: Optional[List[ArtigoSchema]] = None

class UsuarioSchemaUpdate(BaseModel):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    eh_admin: Optional[bool]

    
