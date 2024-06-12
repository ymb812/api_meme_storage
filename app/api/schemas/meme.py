from datetime import datetime
from pydantic import BaseModel, HttpUrl, UUID4


class MemeDB(BaseModel):
    class Config:
        from_attributes = True

    uuid: UUID4
    title: str
    image_url: str
    created_at: datetime
    updated_at: datetime


class MemeToBeUpdated(BaseModel):
    class Config:
        from_attributes = True

    title: str | None = None
    image_url: str | None = None


class MemeCreate:
    class Request(BaseModel):
        title: str
        image_url: HttpUrl

    class Response(BaseModel):
        status: str
        meme: MemeDB


class MemeUpdate:
    class Request(MemeToBeUpdated):
        pass

    class Response(BaseModel):
        status: str
        meme: MemeDB


class MemeDelete:
    class Response(BaseModel):
        uuid: UUID4
        status: str
