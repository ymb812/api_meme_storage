import logging
from fastapi import APIRouter, HTTPException, status
from tortoise.contrib.fastapi import HTTPNotFoundError
from database.models import Meme
from api.schemas.meme import UUID4, MemeCreate, MemeUpdate, MemeDB, MemeDelete

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[MemeDB]
)
async def get_memes(offset: int = 0, limit: int = 10):
    memes = await Meme.all().offset(offset).limit(limit)
    return (MemeDB.from_orm(meme) for meme in memes)


@router.get(
    '/{uuid}',
    status_code=status.HTTP_200_OK,
    response_model=MemeDB,
    responses={
        404: {'model': HTTPNotFoundError}
    }
)
async def get_meme(uuid: UUID4):
    meme = await Meme.get_or_none(uuid=uuid)
    if not meme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Meme with uuid={uuid} not found',
        )
    return MemeDB.from_orm(meme)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=MemeCreate.Response,
)
async def create_meme(body: MemeCreate.Request):
    meme = await Meme.create(**body.dict())
    return {
        'status': 'Meme has been successfully created',
        'meme': MemeDB.from_orm(meme),
    }


@router.put(
    '/{uuid}',
    status_code=status.HTTP_200_OK,
    response_model=MemeUpdate.Response,
    responses={
        404: {'model': HTTPNotFoundError},
    }
)
async def update_meme(uuid: UUID4, body: MemeUpdate.Request):
    meme = await Meme.get_or_none(uuid=uuid)
    if not meme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Meme with uuid={uuid} not found',
        )

    await meme.update_fields(updated_fields=body)

    return {
        'status': 'Meme has been successfully updated',
        'meme': MemeDB.from_orm(meme),
    }


@router.delete(
    '/{uuid}',
    status_code=status.HTTP_200_OK,
    response_model=MemeDelete.Response,
    responses={
        404: {'model': HTTPNotFoundError},
    }
)
async def delete_meme(uuid: UUID4):
    deleted_count = await Meme.filter(uuid=uuid).delete()
    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Meme with uuid={uuid} not found'
        )

    return {
        'uuid': uuid,
        'status': 'Product was deleted successfully.',
    }
