import requests
import json


def get_card_info(ip, headers, cookies):
    data = {"json": "true"}
    # headers["X_REQUESTED_WITH"] = cookies._cookies[ip]["/"]["pageToken"].value
    r = requests.post(
        url="http://" + ip + "/User/GetCardInfoByAccountNoParm",
        headers=headers,
        cookies=cookies,
        data=data,
    )
    if r.status_code == 200:
        if r.json()["IsSucceed"]:   # 不仅名称是“IsSucceed”，值还和实际意义相反（
            return None
        card_info = json.loads(r.json()["Msg"])["query_card"]["card"][0]
        return card_info
    else:
        return None


def get_card_flow(ip, headers, cookies, data):
    r = requests.post(
        url="http://" + ip + "/Report/GetPersonTrjn",
        headers=headers,
        cookies=cookies,
        data=data,
    )
    return r.json()
