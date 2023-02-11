import json
import csv


class CardFlow:
    def __init__(self, session, ip="202.114.64.162"):
        self._ip = ip
        self._card_info = None
        self._session = session
        self.set_card_info()

    def set_card_info(self):
        r = self._session.post(
            url="http://" + self._ip + "/User/GetCardInfoByAccountNoParm",
            data={"json": "true"},
        )
        if r.status_code == 200 and not r.json()["IsSucceed"]:
            # "IsSucceed" 这一项不仅名称是“IsSucceed”，值还和实际意义相反（
            self._card_info = json.loads(r.json()["Msg"])["query_card"]["card"][0]
        else:
            raise Exception("Failed to get card info from {_ip}")

    def get_card_info(self):
        return self._card_info

    def get_card_flow_raw(self, start_date, end_date, max_items=100, account=""):
        if account == "":
            account = self._card_info["account"]
        data = {
            "sdate": start_date,
            "edate": end_date,
            "account": account,
            "page": "1",
            "rows": max_items,
        }
        r = self._session.post(
            url="http://" + self._ip + "/Report/GetPersonTrjn",
            data=data,
        )
        return r.json()

    def get_card_flow_list(self, start_date, end_date, max_items=100, account=""):
        raw_json = self.get_card_flow_raw(start_date, end_date, max_items, account)[
            "rows"
        ]
        list = []
        for i in raw_json:
            list.append([i["OCCTIME"], i["TRANAMT"], i["MERCNAME"].strip()])
        return list

    def output_csv(
        self, start_date, end_date, output_file="output.csv", max_items=100, account=""
    ):
        flow_list = self.get_card_flow_list(start_date, end_date, max_items, account)
        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(flow_list)
