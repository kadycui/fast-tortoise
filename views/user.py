from email_validator import EmailNotValidError, validate_email
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination.ext.tortoise import paginate
from common.logger import logger
from common.pagination import Page, Params
from control.user_operate import user_db

from schemas.token import Token
from schemas.user import Auth, GetUserInfo, CreateUser
from utils import Response200
from utils import jwt
from utils import verify

user = APIRouter()

headers = {"WWW-Authenticate": "Bearer"}


@user.get("/index", summary="主页")
async def index(request: Request):
    logger.info(f"{request.method} {request.url}")
    data = {"code": 200, "msg": "这是主页"}
    return data


@user.post('/login', summary='表单登录', response_model=Token)
async def user_login(form_data: OAuth2PasswordRequestForm = Depends()):
    current_user = await user_db.get_user_by_username(form_data.username)
    if not current_user:
        raise HTTPException(status_code=404, detail='用户名不存在', headers=headers)
    elif not verify.verity_password(form_data.password, current_user.password):
        raise HTTPException(status_code=401, detail='密码错误', headers=headers)
    elif not current_user.is_active:
        raise HTTPException(status_code=401, detail='用户已被锁定', headers=headers)
    await user_db.update_user_login_time(current_user.pk)
    access_token = jwt.create_access_token(current_user.pk)
    return Token(
        access_token=access_token,
        token_type='Bearer',
        is_superuser=current_user.is_superuser
    )


@user.post("/register", summary="注册", response_model=Response200)
async def create_user(request: Request, obj: CreateUser):
    username = await user_db.get_user_by_username(name=obj.username)
    if username:
        raise HTTPException(status_code=403, detail="该用户名已被注册~")
    email = await user_db.check_email(email=obj.email)
    if email:
        raise HTTPException(status_code=403, detail="该邮箱已被注册~")
    try:
        validate_email(obj.email, check_deliverability=False).email
    except EmailNotValidError:
        raise HTTPException(status_code=403, detail="邮箱格式错误，请重新输入")
    new_user = await user_db.register_user(obj)
    new_user.creator = request.client.host
    await new_user.save()
    data = await GetUserInfo.from_tortoise_orm(new_user)
    return Response200(data=data)


@user.get('/all', summary='获取所有用户', response_model=Page[GetUserInfo],
          dependencies=[Depends(jwt.get_current_user)])
async def get_all_users(params:Params = Depends()):
    all_user = user_db.model.all().order_by('-id')
    return await paginate(all_user, params)


@user.get("/{pk}", summary="获取一个用户", response_model=GetUserInfo, dependencies=[Depends(jwt.get_current_user)])
async def get_user(pk: int):
    user = await user_db.get_user_by_id(pk=pk)
    return Response200(data=user)


@user.delete("/{pk}", summary="删除一个用户", dependencies=[Depends(jwt.get_current_user)])
async def delete_user(pk: int):
    await user_db.delete_user(pk=pk)
    return Response200()
