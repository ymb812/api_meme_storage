from pydantic import BaseModel, Field, SecretStr


class APPSettings(BaseModel):
    prod_mode: bool = Field(alias='PROD_MODE_PRIVATE', default=False)
    x_auth_token: SecretStr = Field(alias='X_AUTH_TOKEN')


class DataBaseConfigsModel(BaseModel):
    db_user: str = Field(alias='POSTGRES_USER')
    db_host: str = Field(alias='POSTGRES_HOST')
    db_port: int = Field(alias='POSTGRES_PORT')
    db_pass: SecretStr = Field(alias='POSTGRES_PASSWORD')
    db_name: SecretStr = Field(alias='POSTGRES_DATABASE')


class RestAPISettings(BaseModel):
    rest_host_public: str = Field(alias='REST_HOST_PUBLIC')
    rest_host_private: str = Field(alias='REST_HOST_PRIVATE')
    rest_port_public: int = Field(alias='REST_PORT_PUBLIC')
    rest_port_private: int = Field(alias='REST_PORT_PRIVATE')


class ImageUploadSettings(BaseModel):
    part_size_in_bytes: int = Field(alias='PART_SIZE_IN_BYTES', default=10 * 1024 * 1024)

class S3Settings(BaseModel):
    s3_endpoint_url: str = Field(alias='S3_ENDPOINT_URL')
    s3_bucket_name: str = Field(alias='S3_BUCKET_NAME')
    s3_access_key: SecretStr = Field(alias='S3_ACCESS_KEY')
    s3_secret_key: SecretStr = Field(alias='S3_SECRET_KEY')
    s3_is_secure: bool = Field(alias='S3_IS_SECURE')


class Settings(
    APPSettings,
    DataBaseConfigsModel,
    RestAPISettings,
    ImageUploadSettings,
    S3Settings,
):
    pass
