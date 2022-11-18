import flow
import time
from get_cookie import get_cookie

ip = "202.114.64.162"

data = {
    "sdate": "",
    "edate": "",
    "account": "",
    "page": "1",
    "rows": "15",
}

data["sdate"]=time.strftime("%Y-%m-%d", time.localtime())
data["edate"]=time.strftime("%Y-%m-%d", time.localtime())

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Content-Length": "63",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": ip,
    "Origin": "http://" + ip,
    "Proxy-Connection": "keep-alive",
    "Referer": "http://" + ip + "/Page/Page",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

cookie=get_cookie(ip)

data["account"]=flow.get_card_info(ip, headers, cookie)["account"]

print(flow.get_card_flow(ip, headers, cookie, data)["rows"])
