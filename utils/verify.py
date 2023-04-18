from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')  # 密码加密


def get_hash_password(password: str) -> str:
    """
    使用hash算法加密密码
    :param password: 密码
    :return: 加密后的密码
    """
    return pwd_context.hash(password)


def verity_password(plain_password: str, hashed_password: str) -> bool:
    """
    密码校验
    :param plain_password: 要验证的密码
    :param hashed_password: 要比较的hash密码
    :return: 比较密码之后的结果
    """
    return pwd_context.verify(plain_password, hashed_password)
