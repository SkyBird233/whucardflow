from src.whulogin import CardLoginSession
from src.cardflow import CardFlow
import time
from src import qianji

username = input("Username:")
password = input("Password:")

start_date = time.strftime("%Y-%m-%d", time.localtime())
end_date = time.strftime("%Y-%m-%d", time.localtime())

card_login_session = CardLoginSession(username, password)
card_flow = CardFlow(card_login_session)
# cardFlow.getCardFlow(startDate, endDate)

qianji.main(card_flow.get_card_flow(start_date, end_date)["rows"])
