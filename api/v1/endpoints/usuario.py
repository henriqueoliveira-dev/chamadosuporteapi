from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.auth import autenticar_usuario, criar_token_acesso
from core.deps import get_current_user, get_session
from core.security import gerar_hash_senha
from models.usuario_model import UsuarioModel
from schemas.usuario_schema import (
    UsuarioSchemaArtigos,
    UsuarioSchemaCreate,
    UsuarioSchemaRead,
    UsuarioSchemaUpdate,
)

router = APIRouter()


def _require_admin(usuario: UsuarioModel) -> None:
    if not usuario.eh_adm:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores.",
        )


@router.get("/logado", response_model=UsuarioSchemaRead)
async def get_logado(
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    return usuario_logado


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UsuarioSchemaRead,
)
async def post_usuario(
    usuario: UsuarioSchemaCreate,
    db: AsyncSession = Depends(get_session),
):
    novo_usuario = UsuarioModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha),
    )
    db.add(novo_usuario)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um usuário com este email cadastrado.",
        )
    await db.refresh(novo_usuario)
    return novo_usuario


@router.get("/", response_model=List[UsuarioSchemaRead])
async def get_usuarios(
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    _require_admin(usuario_logado)
    result = await db.execute(select(UsuarioModel))
    return result.scalars().unique().all()


@router.get(
    "/{usuario_id}",
    response_model=UsuarioSchemaArtigos,
    status_code=status.HTTP_200_OK,
)
async def get_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    result = await db.execute(
        select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
    )
    usuario = result.scalars().unique().one_or_none()
    if usuario is None:
        raise HTTPException(
            detail="Usuário não encontrado.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    if usuario.id != usuario_logado.id and not usuario_logado.eh_adm:
        raise HTTPException(
            detail="Você não tem permissão para consultar este usuário.",
            status_code=status.HTTP_403_FORBIDDEN,
        )
    return usuario


@router.put(
    "/{usuario_id}",
    response_model=UsuarioSchemaRead,
    status_code=status.HTTP_202_ACCEPTED,
)
async def put_usuario(
    usuario_id: int,
    usuario: UsuarioSchemaUpdate,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    result = await db.execute(
        select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
    )
    usuario_up: Optional[UsuarioModel] = result.scalars().unique().one_or_none()
    if usuario_up is None:
        raise HTTPException(
            detail="Usuário não encontrado.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    if usuario_up.id != usuario_logado.id and not usuario_logado.eh_adm:
        raise HTTPException(
            detail="Você não tem permissão para alterar este usuário.",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    updates = usuario.model_dump(exclude_unset=True)
    if updates.get("eh_admin") is not None:
        _require_admin(usuario_logado)
        usuario_up.eh_adm = updates.pop("eh_admin")

    updates.pop("eh_admin", None)
    for field, value in updates.items():
        # Null means "not provided" for optional fields; don't violate NOT NULL.
        if value is not None:
            setattr(usuario_up, field, gerar_hash_senha(value) if field == "senha" else value)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um usuário com este email cadastrado.",
        )
    await db.refresh(usuario_up)
    return usuario_up


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    result = await db.execute(
        select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
    )
    usuario_del = result.scalars().unique().one_or_none()
    if usuario_del is None:
        raise HTTPException(
            detail="Usuário não encontrado.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    if usuario_del.id != usuario_logado.id and not usuario_logado.eh_adm:
        raise HTTPException(
            detail="Você não tem permissão para excluir este usuário.",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    await db.delete(usuario_del)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    usuario = await autenticar_usuario(
        email=form_data.username,
        senha=form_data.password,
        db=db,
    )
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Dados de acesso incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "access_token": criar_token_acesso(sub=str(usuario.id)),
        "token_type": "bearer",
    }
