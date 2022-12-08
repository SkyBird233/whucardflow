import flow
import time
import login
import qianji

ip = "202.114.64.162"

username = input("username: ")
password = input("password: ")

sdate = time.strftime("%Y-%m-%d", time.localtime())
edate = time.strftime("%Y-%m-%d", time.localtime())

session = login.caslogin(username, password)
if session == None:
    print("caslogin failed")
    exit(1)

session = login.mainlogin(ip, session)

card_info = flow.get_card_info(ip, session)
card_flow = flow.get_card_flow(ip, session, sdate, edate, card_info["account"])

qianji.main(card_flow["rows"])
