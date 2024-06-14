import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from minio import S3Error
from private_api.service.minio_handler import MinioHandler

logger = logging.getLogger(__name__)
router = APIRouter()
minio_handler = MinioHandler.get_instance()


@router.on_event('startup')
async def startup_event():
    try:
        minio_handler.get_or_create_bucket()
    except S3Error as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


@router.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    try:
        data_file = await minio_handler.put_object(file=file)
        return {'url': data_file['url']}
    except S3Error as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Unexpected error: {exc}')
