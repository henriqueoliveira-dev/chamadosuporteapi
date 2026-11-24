from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.configs import settings
from core.security import verificar_senha
from models.usuario_model import UsuarioModel

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
)


async def autenticar_usuario(
    email: EmailStr, senha: str, db: AsyncSession
) -> Optional[UsuarioModel]:
    query = select(UsuarioModel).filter(UsuarioModel.email == email)
    result = await db.execute(query)
    usuario: Optional[UsuarioModel] = result.scalars().unique().one_or_none()

    if usuario is None or not usuario.ativo:
        return None

    if not verificar_senha(senha, usuario.senha):
        return None

    return usuario


def criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    agora = datetime.now(timezone.utc)
    payload = {
        "type": tipo_token,
        "exp": agora + tempo_vida,
        "iat": agora,
        "sub": str(sub),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def criar_token_acesso(sub: str) -> str:
    return criar_token(
        tipo_token="access_token",
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )
