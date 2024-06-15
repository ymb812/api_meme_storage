from pydantic import BaseModel, Field, SecretStr


class APPSettings(BaseModel):
    prod_mode: bool = Field(alias='PROD_MODE_PUBLIC', default=False)
    x_auth_token: SecretStr = Field(alias='X_AUTH_TOKEN')
    upload_file_route: str = Field(alias='UPLOAD_FILE_ROUTE')


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


class Settings(
    APPSettings,
    DataBaseConfigsModel,
    RestAPISettings,
):
    pass
