from pydantic import BaseModel, Field, SecretStr


class APPSettings(BaseModel):
    prod_mode: bool = Field(alias='PROD_MODE', default=False)


class DataBaseConfigsModel(BaseModel):
    db_user: str = Field(alias='POSTGRES_USER')
    db_host: str = Field(alias='POSTGRES_HOST')
    db_port: int = Field(alias='POSTGRES_PORT')
    db_pass: SecretStr = Field(alias='POSTGRES_PASSWORD')
    db_name: SecretStr = Field(alias='POSTGRES_DATABASE')


class RestAPISettings(BaseModel):
    rest_host: str = Field(alias='REST_HOST')
    rest_port: int = Field(alias='REST_PORT')


class ImageUploadSettings(BaseModel):
    max_file_size_in_bytes: int = Field(alias='MAX_FILE_SIZE_IN_BYTES')


class S3Settings(BaseModel):
    s3_endpoint_url: str = Field(alias='S3_ENDPOINT_URL')
    s3_image_bucket_name: str = Field(alias='S3_IMAGE_BUCKET_NAME')
    s3_key_id: SecretStr = Field(alias='S3_KEY_ID')
    s3_secret_key: SecretStr = Field(alias='S3_SECRET_KEY')


class Settings(
    APPSettings,
    DataBaseConfigsModel,
    RestAPISettings,
    ImageUploadSettings,
    S3Settings,
):
    pass
