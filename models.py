from tortoise.models import Model
from tortoise import fields


class Weather(Model):
    id = fields.IntField(pk=True)
    city = fields.CharField(max_length=255, index=True)
    temperature = fields.FloatField()
    description = fields.CharField(max_length=255)
    humidity = fields.IntField()
    wind_speed = fields.FloatField()
    sunrise = fields.DatetimeField()
    sunset = fields.DatetimeField()
    timestamp = fields.DatetimeField(auto_now_add=True)
