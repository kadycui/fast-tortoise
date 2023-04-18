from typing import Any
import time
import datetime
from tortoise import fields
from tortoise.models import Model
from tortoise.fields import CASCADE, SET_NULL
from fastapi.encoders import jsonable_encoder


class Notice(Model):
    id = fields.IntField(description="公告ID", pk=True)
    client_ver = fields.CharField(description="客户端版本", max_length=50, default="")
    title = fields.CharField(description="消息标题", max_length=200)
    sub_title = fields.CharField(description="消息副标题", max_length=200)
    content = fields.TextField(description="消息内容")
    link_url = fields.CharField(description="消息链接", max_length=100, blank=True)
    begin_time = fields.DatetimeField(description="公告开始时间", default=datetime.datetime.now(), index=True,
                                      null=True)
    end_time = fields.DatetimeField(description="公告过期时间", default=datetime.datetime.now(), index=True, null=True)
    create_time = fields.BigIntField(description="公告时间戳", default=int(time.time()), index=True)
    status = fields.IntField(description="公告状态", default=0)
    pub_ip = fields.CharField(description="操作人IP", max_length=20)
    pub_user = fields.IntField(description="操作人ID", index=True)
    notice_type = fields.IntField(description="类型", default=0)
    intervalSecond = fields.IntField(description="间隔时间", default=0)
    size = fields.CharField(description="显示的size", max_length=20, default="0.9,0.9")
    tag = fields.IntField(description="公告标记", default=0, null=True)
    is_temp = fields.IntField(description="是否开服模版", default=0)
    sort = fields.IntField(description="公告排序", default=0, null=True)
    photo_id = fields.IntField(description="推送公告图片ID", default=0, null=True)
    jump = fields.CharField(description="跳转函数", max_length=100, null=True)
    audit_status = fields.SmallIntField(description="审核状态", default=0, null=True)
    http = fields.SmallIntField(description="Http类型", default=0, null=True)

    server: fields.ManyToManyRelation["Server"] = fields.ManyToManyField("models.Server", related_name="notice",
                                                                         on_delete=CASCADE, through="notice_server")
    channel: fields.ManyToManyRelation["Channel"] = fields.ManyToManyField("models.Channel", related_name="notice",
                                                                           on_delete=CASCADE, through="notice_channel")
    group: fields.ManyToManyRelation["Group"] = fields.ManyToManyField("models.Group", related_name="notice",
                                                                       on_delete=CASCADE, through="notice_group")

    def __str__(self):
        return self.title

    class Meta:
        table = "notice"
        ordering = ["-create_time", "id"]


class Channel(Model):
    id = fields.IntField(description="渠道ID", pk=True)
    name = fields.CharField(index=True, max_length=150, description="渠道名")
    channel_key = fields.CharField(index=True, max_length=50, description="渠道key")
    login_key = fields.CharField(max_length=32, description="登录key")
    username = fields.CharField(max_length=20, description="渠道用户名")
    password = fields.CharField(max_length=50, description="渠道密码")
    create_time = fields.DatetimeField(null=True, description="创建时间")
    last_time = fields.DatetimeField(auto_now=True, null=True, description="最后登录时间")
    last_ip = fields.CharField(max_length=20, description="最后登录IP")
    logins = fields.IntField(default=0, description="登录次数")
    agent_name = fields.CharField(max_length=20, default="", index=True, description="渠道平台名", )
    game_app_key = fields.CharField(max_length=50, index=True, description="游戏APPKEY")
    group_key = fields.CharField(max_length=20, description="渠道平台key")
    group_name = fields.CharField(max_length=20, default="", index=True, description="渠道平台名")
    allow_earn = fields.IntField(default=30000, description="渠道允许的价值数")
    back_rate = fields.IntField(default=0, description="返利比例")
    neimax_charge = fields.IntField(default=0, description="内部号充值金额")
    neimax_resource = fields.IntField(default=0, description="内部号最大资源")
    nologin_day = fields.IntField(default=0, description="未登录天数")
    init_val = fields.IntField(default=0, description="初始渠道价值")
    whitelist = fields.IntField(default=0, description="渠道白名单")
    group: fields.ForeignKeyRelation["Group"] = fields.ForeignKeyField("models.Group", related_name="channel",
                                                                       to_field="id", on_delete=SET_NULL, null=True)
    server: fields.ManyToManyRelation["Server"] = fields.ManyToManyField("models.Server", related_name="channel",
                                                                         on_delete=CASCADE,
                                                                         through="channel_server")
    notice: fields.ManyToManyRelation["Notice"]

    def get_channel_json(self):
        return jsonable_encoder(self)

    def __str__(self):
        return self.name

    class Meta:
        table = "channel"
        ordering = ["-create_time", "id"]


class Server(Model):
    id = fields.IntField(description="服务器ID", pk=True)
    client_ver = fields.CharField(max_length=50, description="客户端版本")
    name = fields.CharField(max_length=50, unique=True, description="服务器名称", null=True)
    alias = fields.CharField(max_length=50, description="服务器别名")
    game_addr = fields.CharField(max_length=20, description="服务器别名")
    game_port = fields.IntField(default=0, description="服务器端口")
    log_db_config = fields.CharField(max_length=1000, description="日志库配置")
    report_url = fields.CharField(max_length=100, description="战报地址")
    status = fields.IntField(default=0, description="服务器状态")
    create_time = fields.DatetimeField(auto_now_add=True, description="开服时间", null=True)
    require_ver = fields.IntField(default=0, description="需要客户端最低版本")
    remark = fields.CharField(max_length=200, description="备注", )
    json_data = fields.CharField(default="", max_length=1000, description="附加JSON数据")
    order = fields.IntField(default=0, description="排序", )
    commend = fields.IntField(default=0, description="推荐")
    is_ios = fields.IntField(default=0, description="是否IOS服务器", )
    last_time = fields.DatetimeField(auto_now_add=True, description="最后修改时间", null=True)
    tabId = fields.IntField(default=0, description="分组ID", null=True)
    game_data = fields.CharField(default="", max_length=1000, description="游戏里的JSON数据(战力,等级)", null=True)
    battleplan_id = fields.IntField(default=0, description="跨服组ID", null=True)
    season_group_id = fields.IntField(default=0, description="赛季组ID", null=True)
    real_number = fields.IntField(default=0, description="当前注册人数", null=True)
    expect_time = fields.IntField(default=-1, description="注册开关时间", null=True)
    expect_number = fields.IntField(default=-1, description="注册开关账号数", null=True)
    switch_status = fields.IntField(default=0, description="注册开关状态", null=True)
    open_server_status = fields.IntField(default=0, description="开服状态", null=True)
    channel: fields.ManyToManyRelation["Channel"]
    notice: fields.ManyToManyRelation["Notice"]

    def get_server_json(self):
        return jsonable_encoder(self)

    def __str__(self):
        return self.name

    class Meta:
        table = "server"
        ordering = ["-create_time", "id"]


class Group(Model):
    id = fields.IntField(description="分区ID", pk=True)
    group_key = fields.CharField(max_length=50, description="分区KEY", unique=True, index=True)
    name = fields.CharField(max_length=50, description="分区名", unique=True)
    login_url = fields.CharField(description="登陆服地址", max_length=100)
    card_url = fields.CharField(description="礼包卡地址", max_length=100)
    notice_url = fields.CharField(description="公告地址", max_length=100)
    cdn_url = fields.CharField(description="cdn地址", max_length=100)
    notice_select = fields.IntField(description="分区公告", default=0)
    remark = fields.CharField(description="备注", max_length=200, null=True)
    other = fields.CharField(description="附加json", max_length=500, null=True)
    pid_list = fields.CharField(description="联运ID列表", max_length=500)
    version = fields.IntField(description="版本号", null=True)
    custom_url = fields.CharField(description="客服地址", max_length=100, null=True)
    sdk_url = fields.CharField(description="平台地址", max_length=100, null=True)
    audit_version = fields.IntField(description="审核版本", null=True)
    audit_server = fields.IntField(description="审核服", null=True)
    create_time = fields.DatetimeField(auto_now_add=True, null=True, description="创建时间")
    last_time = fields.DatetimeField(auto_now=True, null=True, description="最后修改时间")
    resource_version = fields.IntField(description="资源版本号", null=True)
    audit_versions = fields.CharField(description="审核版本", max_length=100, null=True)
    audit_servers = fields.CharField(description="审核服s", max_length=100, null=True)
    game_app_key = fields.CharField(description="游戏APPKEY", max_length=50, null=True)  # 新后台需要game_app_key
    expect_number = fields.IntField(description="注册开关账号数", default=-1, null=True)
    expect_time = fields.IntField(description="注册开关时间", default=-1, null=True)
    switch_status = fields.IntField(description="注册开关状态", default=0, null=True)
    switch_last_time = fields.DatetimeField(description="注册开关修改时间", null=True)
    channel: fields.ReverseRelation["Channel"]
    notice: fields.ManyToManyRelation["Notice"]

    def __str__(self):
        return self.name

    class Meta:
        table = "group"
        ordering = ["-create_time", "id"]
