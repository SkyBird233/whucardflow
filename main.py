from whulogin import CardLoginSession
from cardflow import CardFlow
import time
import qianji

username = input("Username:")
password = input("Password:")

startDate = time.strftime("%Y-%m-%d", time.localtime())
endDate = time.strftime("%Y-%m-%d", time.localtime())

cardLoginSession = CardLoginSession(username, password)
cardFlow = CardFlow(cardLoginSession)
# cardFlow.getCardFlow(startDate, endDate)

qianji.main(cardFlow.getCardFlow(startDate, endDate)["rows"])