import logging
from datetime import datetime, timedelta
from minio import Minio, S3Error
from private_api.settings.settings import settings
from fastapi import UploadFile
import io

logger = logging.getLogger(__name__)


class MinioHandler:
    __instance = None

    def __init__(self):
        self.minio_url = settings.s3_endpoint_url
        self.access_key = settings.s3_access_key.get_secret_value()
        self.secret_key = settings.s3_secret_key.get_secret_value()
        self.bucket_name = settings.s3_bucket_name
        self.is_secure = settings.s3_is_secure
        self.client = Minio(
            self.minio_url,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.is_secure,
        )
        self.get_or_create_bucket()

    @staticmethod
    def get_instance():
        if not MinioHandler.__instance:
            MinioHandler.__instance = MinioHandler()
        return MinioHandler.__instance

    def get_or_create_bucket(self) -> str:
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
            return self.bucket_name
        except S3Error as e:
            logger.error(f'Error creating/getting bucket: {self.bucket_name}', exc_info=e)
            raise

    async def put_object(self, file: UploadFile):
        try:
            datetime_prefix = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
            object_name = f'{datetime_prefix}___{file.filename}'

            # get file content
            content = await file.read()
            file_size = len(content)
            file_stream = io.BytesIO(content)

            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=file_stream,
                length=file_size,
                part_size=10 * 1024 * 1024
            )
            url = self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                expires=timedelta(days=7),
            )
            data_file = {
                'bucket_name': self.bucket_name,
                'file_name': object_name,
                'url': url,
            }
            return data_file

        except Exception as e:
            logger.error('Error putting object to Minio', exc_info=e)
            raise
