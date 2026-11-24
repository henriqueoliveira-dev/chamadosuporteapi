from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.auth import oauth2_schema
from core.configs import settings
from core.database import async_session
from models.usuario_model import UsuarioModel


def _credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = async_session()
    try:
        yield session
    finally:
        await session.close()


get_db = get_session


async def get_current_user(
    token: str = Depends(oauth2_schema),
    db: AsyncSession = Depends(get_session),
) -> UsuarioModel:
    credentials_exception = _credentials_exception()

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
        )
        subject = payload.get("sub")
        if payload.get("type") != "access_token" or subject is None:
            raise credentials_exception
        user_id = int(subject)
    except (JWTError, TypeError, ValueError):
        raise credentials_exception

    query = select(UsuarioModel).filter(UsuarioModel.id == user_id)
    result = await db.execute(query)
    usuario = result.scalars().unique().one_or_none()

    if usuario is None or not usuario.ativo:
        raise credentials_exception

    return usuario
