from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel
from schemas.artigo_schema import ArtigoSchema
from core.deps import get_session, get_current_user


router = APIRouter()

# POST Artigo
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def post_artigo(artigo: ArtigoSchema, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    novo_artigo: ArtigoModel = ArtigoModel(titulo=artigo.titulo, descricao=artigo.descricao, url_fonte=str(artigo.url_fonte), data_criacao=datetime.now(), usuario_id=usuario_logado.id)

    db.add(novo_artigo)
    await db.commit()

    return novo_artigo

# GET Artigos
@router.get('/', response_model=List[ArtigoSchema])
async def get_artigos(db: AsyncSession = Depends(get_session)):
    query = select(ArtigoModel)
    result = await db.execute(query)
    artigos: List[ArtigoModel] = result.scalars().unique().all()

    return artigos


#GET Artigo
@router.get('/{artigo_id}', response_model=ArtigoSchema, status_code=status.HTTP_200_OK)
async def get_artigo(artigo_id:int, db:AsyncSession= Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().unique().one_or_none()

        if artigo:
            return artigo
        else:
            raise HTTPException(detail='Artigo não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
#POT Artigo
@router.put('/{artigo_id}', response_model=ArtigoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_artigo(artigo_id:int, artigo: ArtigoSchema, db:AsyncSession= Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo_up: ArtigoModel = result.scalars().unique().one_or_none()

        if not artigo_up:
            raise HTTPException(detail='Artigo não encontrado', status_code=status.HTTP_404_NOT_FOUND)

        if artigo_up.usuario_id != usuario_logado.id:
            raise HTTPException(detail='Você não tem permissão para alterar este artigo', status_code=status.HTTP_403_FORBIDDEN)

        artigo_up.titulo = artigo.titulo
        artigo_up.descricao = artigo.descricao
        artigo_up.url_fonte = str(artigo.url_fonte)

        if artigo.usuario_id is not None:
            usuario_query = select(UsuarioModel).filter(UsuarioModel.id == artigo.usuario_id)
            usuario_result = await session.execute(usuario_query)
            novo_usuario = usuario_result.scalars().unique().one_or_none()
            if not novo_usuario:
                raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
            artigo_up.usuario_id = novo_usuario.id

        await session.commit()
        await session.refresh(artigo_up)
        return artigo_up
        
    
#Delete Artigo
@router.delete('/{artigo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(artigo_id:int, db:AsyncSession= Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo_del: ArtigoModel = result.scalars().unique().one_or_none()

        if not artigo_del:
            raise HTTPException(detail='Artigo não encontrado', status_code=status.HTTP_404_NOT_FOUND)

        if artigo_del.usuario_id != usuario_logado.id:
            raise HTTPException(
                detail='Você não tem permissão para excluir este artigo',
                status_code=status.HTTP_403_FORBIDDEN,
            )

        await session.delete(artigo_del)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
