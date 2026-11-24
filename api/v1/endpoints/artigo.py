from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_current_user, get_session
from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel
from schemas.artigo_schema import ArtigoSchema

router = APIRouter()


def _artigo_nao_encontrado() -> HTTPException:
    return HTTPException(
        detail="Artigo não encontrado",
        status_code=status.HTTP_404_NOT_FOUND,
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def post_artigo(
    artigo: ArtigoSchema,
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    novo_artigo = ArtigoModel(
        titulo=artigo.titulo,
        descricao=artigo.descricao,
        url_fonte=str(artigo.url_fonte),
        data_criacao=datetime.now(),
        usuario_id=usuario_logado.id,
    )
    db.add(novo_artigo)
    await db.commit()
    await db.refresh(novo_artigo)
    return novo_artigo


@router.get("/", response_model=List[ArtigoSchema])
async def get_artigos(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(ArtigoModel))
    return result.scalars().unique().all()


@router.get(
    "/{artigo_id}",
    response_model=ArtigoSchema,
    status_code=status.HTTP_200_OK,
)
async def get_artigo(artigo_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
    )
    artigo = result.scalars().unique().one_or_none()
    if artigo is None:
        raise _artigo_nao_encontrado()
    return artigo


@router.put(
    "/{artigo_id}",
    response_model=ArtigoSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def put_artigo(
    artigo_id: int,
    artigo: ArtigoSchema,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    result = await db.execute(
        select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
    )
    artigo_up = result.scalars().unique().one_or_none()
    if artigo_up is None:
        raise _artigo_nao_encontrado()
    if artigo_up.usuario_id != usuario_logado.id:
        raise HTTPException(
            detail="Você não tem permissão para alterar este artigo",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    artigo_up.titulo = artigo.titulo
    artigo_up.descricao = artigo.descricao
    artigo_up.url_fonte = str(artigo.url_fonte)
    # Ownership is assigned at creation and cannot be transferred via a PUT body.
    await db.commit()
    await db.refresh(artigo_up)
    return artigo_up


@router.delete("/{artigo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(
    artigo_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    result = await db.execute(
        select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
    )
    artigo_del = result.scalars().unique().one_or_none()
    if artigo_del is None:
        raise _artigo_nao_encontrado()
    if artigo_del.usuario_id != usuario_logado.id:
        raise HTTPException(
            detail="Você não tem permissão para excluir este artigo",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    await db.delete(artigo_del)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
