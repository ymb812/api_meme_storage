import logging
from fastapi import APIRouter, UploadFile, HTTPException, status, Header, Depends
from minio import S3Error
from private_api.api.schemas.media_upload import MediaUpload
from private_api.service.minio_handler import MinioHandler
from private_api.settings.settings import settings


def authorize_user(X_AUTH_TOKEN: str = Header(None)):
    if X_AUTH_TOKEN != settings.x_auth_token.get_secret_value():
        raise HTTPException(status_code=401, detail='Unauthorized')
    return True


logger = logging.getLogger(__name__)
router = APIRouter(dependencies=[Depends(authorize_user)])
minio_handler = MinioHandler.get_instance()


@router.on_event('startup')
async def startup_event():
    try:
        minio_handler.get_or_create_bucket()
    except S3Error as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


@router.post(
    '/upload',
    status_code=status.HTTP_200_OK,
    response_model=MediaUpload.Response,
    responses={
        400: {'description': 'Filename must be < 255 bytes'}
    },
)
async def upload_file(file: UploadFile):
    # check minio limits for filename
    if len(file.filename.encode('utf-8')) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Filename must be < 255 bytes, rename and try again'
        )

    try:
        data_file = await minio_handler.put_object(file=file)

    except S3Error as e:
        logger.error('Error with S3', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    except Exception as e:
        logger.error('Unexpected error with s3 /upload', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Unexpected error: {e}')

    return MediaUpload.Response(**data_file)
