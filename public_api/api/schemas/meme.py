from datetime import datetime
from pydantic import BaseModel, UUID4


class MemeDB(BaseModel):
    class Config:
        from_attributes = True

    uuid: UUID4
    title: str
    media_url: str
    created_at: datetime
    updated_at: datetime


class MemeToBeUpdated(BaseModel):
    class Config:
        from_attributes = True

    title: str | None = None
    media_url: str | None = None


class MemeCreate:
    class Request(BaseModel):
        pass

    class Response(BaseModel):
        status: str
        meme: MemeDB


class MemeUpdate:
    class Request(BaseModel):
        pass

    class Response(BaseModel):
        status: str
        meme: MemeDB


class MemeDelete:
    class Response(BaseModel):
        uuid: UUID4
        status: str


class MediaUpload:
    class Request(BaseModel):
        pass

    class Response(BaseModel):
        bucket_name: str
        file_name: str
        url: str
