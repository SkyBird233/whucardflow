import browser_cookie3

def browser_cookie(url):
    return browser_cookie3.load(domain_name=url)

def get_cookie(ip):
    return browser_cookie(ip)
    # 检查配置文件，可能从配置读取cookie