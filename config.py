import os
import json

def get_config():
    with open('cookies.json','r') as f:
        cookies = f.read()
        # print(cookies)
    nickname = os.getenv("NICKNAME")
    msg = os.getenv("MSG","火花")
    proxy = os.getenv("PROXY")

    print(proxy)

    if proxy is '':
        proxy = None
    else:
        proxy = json.loads(proxy)

    if cookies is '' or nickname is '':
        raise ValueError("SECRETS 未正确配置！")

    return {
        'cookies' : cookies,
        'nickname' : nickname,
        'msg' : msg,
        'proxy' : proxy
    }