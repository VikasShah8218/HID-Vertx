from tortoise import fields
from tortoise.models import Model

class VertxLog(Model):
    id = fields.BigIntField(pk=True)
    log = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "vertx_logs"
