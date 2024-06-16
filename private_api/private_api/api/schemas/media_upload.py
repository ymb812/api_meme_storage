from pydantic import BaseModel


class MediaUpload:
    class Request(BaseModel):
        pass

    class Response(BaseModel):
        bucket_name: str
        file_name: str
        url: str
