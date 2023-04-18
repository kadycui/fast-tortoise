import time
import hashlib


def md5(sign_str: str) -> str:
    """md5加密"""
    return hashlib.md5(sign_str.encode(encoding='utf-8')).hexdigest()


