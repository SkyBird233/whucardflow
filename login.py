import requests
import aes_sp
from time import time
from bs4 import BeautifulSoup


# 直接登录校园开服务大厅需要验证码，跳转校内使用统一身份认证登录不用
def caslogin(username, password):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    }
    session = requests.Session()
    session.headers.update(headers)

    # 从第一次请求获取密钥和 lt
    r = session.get("https://cas.whu.edu.cn/authserver/login")
    soup = BeautifulSoup(r.text, "html.parser")
    key = soup.find("input", {"id": "pwdDefaultEncryptSalt"})["value"]
    ## 虽然关键字是 pwdDefaultEncryptSalt，但是实际上是密钥（
    lt = soup.find("input", {"name": "lt"})["value"]

    # 检查是否需要验证码，内网连接时一般不需要验证码，两个请求均返回 false
    params = {
        "username": username,
        "pwdEncrypt2": "pwdEncryptSalt",
        "_": int(time() * 1000),
    }
    needDxCaptcha = session.get(
        "https://cas.whu.edu.cn/authserver/needDxCaptcha.html", params=params
    ).text.strip()  ## 是否需要未知验证码
    params["_"] = int(time() * 1000)
    needCaptcha = session.get(
        "https://cas.whu.edu.cn/authserver/needCaptcha.html", params=params
    ).text  ## 是否需要滑块验证码

    if needDxCaptcha == "true" or needCaptcha == "true":
        print("需要验证码")
        return

    # 构造表单
    form = {
        "username": username,
        "password": aes_sp.encrypt(password, key),
        "lt": lt,
        "dllt": "userNamePasswordLogin",
        "execution": "e1s1",
        "_eventId": "submit",
        "rmShown": "1",
    }

    # 登录
    r = session.post(
        url="https://cas.whu.edu.cn/authserver/login", data=form, headers=headers
    )
    if r.url != "https://cas.whu.edu.cn/authserver/index.do":
        print("登录失败")
        return
    return session


# 得先登录统一身份认证，绕过验证码
def mainlogin(ip, session):
    url = "http://" + ip + "/cassyno/index"
    r = session.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    ssoticketid = soup.find("input", {"id": "ssoticketid"})["value"]
    # ssoticketid 在返回内容(js)里不在 cookies 里，得重新构造个请求

    form = {"errorcode": "1", "continueurl": url, "ssoticketid": ssoticketid}

    r = session.post(url, data=form)
    if r.url != "http://" + ip + "/user/user":
        print("mainlogin failed")
        return

    return session
