import logging
import aiohttp
import io
from fastapi import APIRouter, HTTPException, status, UploadFile
from public_api.database.models import Meme
from public_api.api.schemas.meme import (
    UUID4,
    MemeCreate,
    MemeUpdate,
    MemeToBeUpdated,
    MemeDB,
    MemeDelete,
    MediaUpload,
)
from public_api.settings.settings import settings

logger = logging.getLogger(__name__)
router = APIRouter()


async def upload_media(file: UploadFile) -> MediaUpload.Response:
    try:
        contents = await file.read()
        byte_stream = io.BytesIO(contents)
        form_data = aiohttp.FormData(quote_fields=False)
        form_data.add_field('file', byte_stream, filename=file.filename, content_type=file.content_type)

        # request to the private API
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=settings.upload_file_route.format(
                        rest_host_private=settings.rest_host_private, rest_port_private=settings.rest_port_private
                    ),
                    data=form_data,
                    headers={
                        'X-AUTH-TOKEN': settings.x_auth_token.get_secret_value()
                    },
            ) as response:
                if response.status != 200:
                    logger.error(f'Error uploading image: status={response.status}, response={await response.text()}')
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT, detail='Cannot upload image via internal service'
                    )
                file_data = MediaUpload.Response(**await response.json())

    except Exception as e:
        logger.error(f'Cannot upload image', exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Cannot upload image via internal service'
        )

    return file_data


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
        404: {'description': 'Meme not found'},
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
    responses={
        409: {'description': 'Cannot upload image via internal service'}
    },
)
async def create_meme(title: str, file: UploadFile):
    file_data = await upload_media(file=file)

    meme = await Meme.create(
        title=title,
        media_url=file_data.url,
    )

    return {
        'status': 'Meme has been successfully created',
        'meme': MemeDB.from_orm(meme),
    }


@router.put(
    '/{uuid}',
    status_code=status.HTTP_200_OK,
    response_model=MemeUpdate.Response,
    responses={
        404: {'description': 'Meme not found'},
        409: {'description': 'Cannot upload image via internal service'}
    }
)
async def update_meme(uuid: UUID4, title: str = None, file: UploadFile = None):
    meme = await Meme.get_or_none(uuid=uuid)
    if not meme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Meme with uuid={uuid} not found',
        )

    media_url = None
    if file:
        file_data = await upload_media(file=file)
        media_url = file_data.url

    # update meme
    await meme.update_fields(updated_fields=MemeToBeUpdated(
        title=title,
        media_url=media_url
    ))

    return {
        'status': 'Meme has been successfully updated',
        'meme': MemeDB.from_orm(meme),
    }


@router.delete(
    '/{uuid}',
    status_code=status.HTTP_200_OK,
    response_model=MemeDelete.Response,
    responses={
        404: {'description': 'Meme not found'},
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
        'status': 'Meme has been successfully deleted',
    }
