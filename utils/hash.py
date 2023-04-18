from uuid import uuid4

from utils.verify import pwd_context


def use_uuid() -> str:
    """
    生成uuid字符串
    :return:
    """
    return uuid4().hex


def get_hash_password(password: str) -> str:
    """
    使用hash算法加密密码
    :param password: 密码
    :return: 加密后的密码
    """
    return pwd_context.hash(password)
