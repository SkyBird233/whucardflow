import requests
from bs4 import BeautifulSoup
from time import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode
from random import choices


class CasLoginSession(requests.Session):
    """
    统一身份认证登录
    """

    def __init__(self, username, password):
        super().__init__()
        self.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            }
        )
        self.__username = username
        self.__password = password
        self.__key = None
        self.__lt = None

    def __getKeys(self):
        # 从第一次请求获取密钥和 lt
        r = self.get("https://cas.whu.edu.cn/authserver/login")
        soup = BeautifulSoup(r.text, "html.parser")
        key = soup.find("input", {"id": "pwdDefaultEncryptSalt"})[
            "value"
        ]  # 虽然关键字是 pwdDefaultEncryptSalt，但是实际上是密钥（
        lt = soup.find("input", {"name": "lt"})["value"]

        self.__key = key
        self.__lt = lt

    def __encrypt(self, data, key):
        # 加密方式：AES-128-CBC，密钥长度：16，偏移量长度：16，填充方式：PKCS7Padding，密文前 64 位随机字符串
        chars = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678"  # 原 js 这么写的
        data = ("".join(choices(chars, k=64)) + data).encode("utf-8")
        key = key.encode("utf-8")
        iv = "".join(choices(chars, k=16)).encode("utf-8")
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        ct = b64encode(ct_bytes).decode("utf-8")
        return ct

    def isCaptchaRequired(self):
        # 检查是否需要验证码。内网连接时一般不需要验证码
        params = {
            "username": self.__username,
            "pwdEncrypt2": "pwdEncryptSalt",
            "_": int(time() * 1000),
        }

        dxCaptcha = self.get(
            "https://cas.whu.edu.cn/authserver/needDxCaptcha.html", params=params
        ).text.strip()

        params["_"] = int(time() * 1000)
        captcha = self.get(
            "https://cas.whu.edu.cn/authserver/needCaptcha.html", params=params
        ).text  # 对应滑块验证码

        return dxCaptcha == "true", captcha == "true"

    def login(self):
        # 要先检查是否需要验证码
        self.__getKeys()

        data = {
            "username": self.__username,
            "password": self.__encrypt(self.__password, self.__key),
            "lt": self.__lt,
            "dllt": "userNamePasswordLogin",
            "execution": "e1s1",
            "_eventId": "submit",
            "rmShown": "1",
        }

        r = self.post("https://cas.whu.edu.cn/authserver/login", data=data)

        return r.url == "https://cas.whu.edu.cn/authserver/index.do"


class CardLoginSession(CasLoginSession):
    """
    通过统一身份认证登录卡系统
    """

    def __init__(self, username, password, ip="202.114.64.162"):
        super().__init__(username, password)
        self.__ip = ip
        self.login()

    def login(self):
        if self.isCaptchaRequired():
            raise Exception("需要验证码")

        if not super().login():
            raise Exception("统一身份认证登录失败")

        url = "http://" + self.__ip + "/cassyno/index"
        soup = BeautifulSoup(self.get(url).text, "html.parser")
        ssoticketid = soup.find("input", {"name": "ssoticketid"})["value"]
        # ssoticketid 在返回内容(js)里不在 cookies 里，得重新构造个请求

        form = {"errorcode": "1", "continueurl": url, "ssoticketid": ssoticketid}

        r = self.post(url, data=form)
        if r.url != "http://" + self.__ip + "/user/user":
            raise Exception("卡系统登录失败")
        else:
            return True
