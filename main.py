from src.whulogin import CardLoginSession
from src.cardflow import CardFlow
from src.config import Config
from src import qianji

config = Config()
if not config.get("username"):
    username = input("Username:")
if not config.get("password"):
    password = input("Password:")

card_login_session = CardLoginSession(config.get("username"), config.get("password"))
card_flow = CardFlow(card_login_session)

if config.get("output_csv"):
    card_flow.output_csv(
        config.get("start_date"),
        config.get("end_date"),
        config.get("output_csv"),
    )

if config.get("standard_output"):
    flow_list = card_flow.get_card_flow_list(config.get("start_date"), config.get("end_date"))
    for item in flow_list:
        for i in item:
            print(i, end="\t")
        print()

if config.get("qianji"):
    qianji.main(
        card_flow.get_card_flow_raw(config.get("start_date"), config.get("end_date"))[
            "rows"
        ]
    )
