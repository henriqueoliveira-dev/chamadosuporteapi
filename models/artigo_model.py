from  sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings

class ArtigoModel(settings.DBBaseModel):
    __tablename__ = "artigos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    url_fonte = Column(String(1000), nullable=False)
    descricao = Column(String(1000), nullable=False)
    data_criacao = Column(DateTime, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    criador = relationship("UsuarioModel", back_populates="artigos", lazy="joined")
    
    