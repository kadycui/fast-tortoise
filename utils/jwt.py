from datetime import datetime, timedelta
from typing import Any, Optional, Union
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from conf.config import settings
from models.user import User
from utils import TokenError, AuthorizationError
from control.user_operate import user_db

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/api/user/login')  # 指明客户端请求token的地址
headers = {"WWW-Authenticate": "Bearer"}  # 异常返回规范


def create_access_token(data: Union[int, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    生成加密 token
    :param data: 传进来的值
    :param expires_delta: 增加的到期时间
    :return: 加密token
    """
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(settings.TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires, "sub": str(data)}
    encoded_jwt = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_schema)) -> User:
    """
    通过token获取当前用户
    :param token:
    :return:
    """
    try:
        # 解密token
        payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        user_id = payload.get('sub')
        if not user_id:
            raise TokenError
    except (jwt.JWTError, ValidationError):
        raise TokenError
    user = await user_db.get_user_by_id(user_id)
    return user


async def get_current_is_superuser(user: User = Depends(get_current_user)) -> User:
    """
    验证当前用户是否为超级用户
    :param user:
    :return:
    """
    if not user.is_superuser:
        raise AuthorizationError
    return await user
