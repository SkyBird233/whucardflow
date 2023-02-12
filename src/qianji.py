import os
import time


def termux_open(uris):
    for uri in uris:
        os.system("termux-open " + '"' + uri + '"')
        time.sleep(3.5)    # 钱迹 api 限制 3 秒只能提交一次


def meal_time(meal_time):
    hour = time.strptime(meal_time, "%Y-%m-%d %H:%M:%S").tm_hour
    if 6 <= hour < 10:
        return "早餐"
    elif 10 <= hour < 14:
        return "午餐"
    elif 14 <= hour < 20:
        return "晚餐"
    else:
        return "零食"


def main(card_flows):
    # 钱迹 api 详见 https://docs.qianjiapp.com/plugin/auto_tasker.html
    uri_head = "qianji://publicapi/addbill?"
    params = {
        "type": "",
        "money": "",
        "time": "",
        "remark": "",  # 备注
        "catename": "",
        "accountname": "",
        "accountname2": "",
    }
    uris = []

    for flow in card_flows:
        params = {k: "" for k in params}  # 清空
        params["time"] = flow["OCCTIME"]  # 时间格式刚好对上，不用转换
        params["remark"] = flow["MERCNAME"].replace(" ", "")
        # 有些记录中间也有无意义空格，所以去除所有空格。不过有待进一步观察
        money = flow["TRANAMT"]

        # money 只接受正数,为 0 时不记 (钱迹不支持账单金额为 0)
        if money > 0:  # 充卡
            params["type"] = "2"
            params["money"] = str(money)
            params["accountname"] = "银行卡"
            params["accountname2"] = "饭卡"
        elif money < 0:
            params["type"] = "0"
            params["money"] = str(-money)
            params["accountname"] = "饭卡"
            if "食堂" in flow["MERCNAME"]:
                params["catename"] = meal_time(flow["OCCTIME"])
            else:
                params["catename"] = "其他"
        else:
            continue

        uri = uri_head
        for k, v in params.items():
            if v != "":
                uri += k + "=" + v + "&"
        uris.append(uri[:-1])  # 去掉最后一个 &

    # for uri in uris:
    #     print(uri)

    termux_open(uris)
