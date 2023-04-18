from tortoise import models
from tortoise import fields


class ModelsBase(models.Model):
    """
    基本模型
    """
    creator = fields.CharField(max_length=32, null=True, verbose_name='创建者', description="创建者")
    modifier = fields.CharField(max_length=32, null=True, verbose_name='修改者', description="修改者")
    created_time = fields.DatetimeField(auto_now_add=True, verbose_name='创建时间', description="创建时间")
    updated_time = fields.DatetimeField(auto_now=True, verbose_name='更新时间', description="更新时间")

    class Meta:
        abstract = True
