import requests
import json


def get_card_info(ip, session):
    # headers["X_REQUESTED_WITH"] = cookies._cookies[ip]["/"]["pageToken"].value
    r = session.post(
        url="http://" + ip + "/User/GetCardInfoByAccountNoParm",
        data={"json": "true"},
    )
    if r.status_code == 200:
        if r.json()["IsSucceed"]:   # 这一项不仅名称是“IsSucceed”，值还和实际意义相反（
            return None
        card_info = json.loads(r.json()["Msg"])["query_card"]["card"][0]
        return card_info
    else:
        return None


def get_card_flow(ip, session, sdate, edate, account):
    data = {
        "sdate": sdate,
        "edate": edate,
        "account": account,
        "page": "1",
        "rows": "15",
    }
    r = session.post(
        url="http://" + ip + "/Report/GetPersonTrjn",
        data=data,
    )
    return r.json()
