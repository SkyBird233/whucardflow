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

main_data = card_flow.get_card_flow(config.get("start_date"), config.get("end_date"))[
    "rows"
]
if config.get("standard_output"):
    print(main_data)
if config.get("qianji"):
    qianji.main(main_data)
