import json


class CardFlow:
    def __init__(self, session, ip="202.114.64.162"):
        self.__ip = ip
        self.__cardInfo = None
        self.session = session

        self.__setCardInfo()

    def __setCardInfo(self):
        r = self.session.post(
            url="http://" + self.__ip + "/User/GetCardInfoByAccountNoParm",
            data={"json": "true"},
        )
        if r.status_code == 200 and not r.json()["IsSucceed"]:  # 这一项不仅名称是“IsSucceed”，值还和实际意义相反（
            self.__card_info = json.loads(r.json()["Msg"])["query_card"]["card"][0]
        else:
            raise Exception("Failed to get card info")

    def getCardFlow(self, startDate, endDate, maxItems=100, account=""):
        if account is "":
            account = self.__card_info["account"]
        data = {
            "sdate": startDate,
            "edate": endDate,
            "account": account,
            "page": "1",
            "rows": maxItems,
        }
        r = self.session.post(
            url="http://" + self.__ip + "/Report/GetPersonTrjn",
            data=data,
        )
        return r.json()
