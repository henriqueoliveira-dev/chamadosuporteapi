from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from core.configs import settings

class UsuarioModel(settings.DBBaseModel):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    sobrenome = Column(String(255), nullable=False)
    email = Column(String(255),index=True, nullable=False, unique=True)
    
    senha = Column(String(255), nullable=False)
    
    eh_adm = Column(Boolean, default=False)

    ativo = Column(Boolean, default=True)
    
    artigos = relationship("ArtigoModel", cascade="all, delete-orphan", back_populates="criador", uselist=True, lazy="joined")  