from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from schemas.artigo_schema import ArtigoSchema


class UsuarioSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    email: EmailStr
    eh_admin: bool = False

    model_config = ConfigDict(from_attributes=True)


class UsuarioSchemaBase(BaseModel):
    senha: str


class UsuarioSchemaRead(BaseModel):
    id: int
    nome: str
    sobrenome: str
    email: EmailStr
    eh_adm: Optional[bool] = None
    ativo: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class UsuarioSchemaCreate(UsuarioSchemaBase):
    nome: str
    sobrenome: str
    email: EmailStr

    # Public sign-up must never silently accept role/privilege fields.
    model_config = ConfigDict(extra="forbid")


class UsuarioSchemaArtigos(UsuarioSchemaRead):
    artigos: Optional[List[ArtigoSchema]] = None


class UsuarioSchemaUpdate(BaseModel):
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    # Kept as the existing update API field; mapped to ORM's eh_adm column.
    eh_admin: Optional[bool] = None
