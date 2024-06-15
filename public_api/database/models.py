from tortoise import fields, models
from public_api.api.schemas.meme import MemeUpdate

class Meme(models.Model):
    class Meta:
        table = 'memes'
        ordering = ['created_at']

    class PydanticMeta:
        pass

    uuid = fields.UUIDField(pk=True)
    title = fields.CharField(max_length=255)
    media_url = fields.CharField(max_length=1023)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


    async def update_fields(self, updated_fields: MemeUpdate.Request):
        updated_data = updated_fields.model_dump(exclude_unset=True)
        for field, value in updated_data.items():
            if hasattr(self, field):
                setattr(self, field, value)

        await self.save()

