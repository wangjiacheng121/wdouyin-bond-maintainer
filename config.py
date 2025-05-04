import os

def get_config():
    cookies = os.getenv("COOKIES")
    nickname = os.getenv("NICKNAME")
    msg = os.getenv("MSG","火花")

    if cookies is None or nickname is None:
        raise ValueError("SECRETS 未正确配置！")

    return {
        'cookies' : cookies,
        'nickname' : nickname,
        'msg' : msg
    }