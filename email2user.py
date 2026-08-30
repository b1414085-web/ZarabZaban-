import requests, json, SignerPy, secrets, uuid, random, time, string, re
from hsopyt import Gorgon, Ladon, Argus, md5, urlencode
from mustafatik import mustafatik

hosts=["api22-normal-c-alisg.tiktokv.com","api31-normal-useast2a.tiktokv.com","api2.musical.ly","api16-normal-c-useast1a.tiktokv.com","http://api16-normal-de.tiktokv.eu"]
def sign(params: str, payload: str or None = None, sec_device_id: str = '', cookie: str or None = None,
         aid: int = 1233, license_id: int = 1611921764, sdk_version_str: str = 'v05.00.06-ov-android',
         sdk_version: int = 167775296, platform: int = 0, unix: float = None):
    x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload is not None else None
    if not unix:
        unix = time.time()
    return Gorgon(params, unix, payload, cookie).get_value() | {
        'content-length': str(len(payload)),
        'x-ss-stub': x_ss_stub.upper(),
        'x-ladon': Ladon.encrypt(int(unix), license_id, aid),
        'x-argus': Argus.get_sign(params, x_ss_stub, int(unix),
                                  platform=platform,
                                  aid=aid,
                                  license_id=license_id,
                                  sec_device_id=sec_device_id,
                                  sdk_version=sdk_version_str,
                                  sdk_version_int=sdk_version)
    }


def email2user(email):
    ss = requests.Session()
    if "@" not in email:email=email+"@gmail.com"
    params = {
        'device_platform': 'android', 'ssmix': 'a', 'channel': 'googleplay',
        'aid': '1233', 'app_name': 'musical_ly', 'version_code': '360505',
        'version_name': '36.5.5', 'manifest_version_code': '2023605050',
        'update_version_code': '2023605050', 'ab_version': '36.5.5',
        'os_version': '10', "device_id": 0, 'app_version': '30.1.2',
        "request_from": "profile_card_v2", "request_from_scene": '1',
        "scene": "1", "mix_mode": "1", "os_api": "34", "ac": "wifi",
        "request_tag_from": "h5", "account_param": email
    }

    signer = mustafatik()
    signer.updateParams(params)
    headers = {
        'User-Agent': f'com.zhiliaoapp.musically/2022703020 (Linux; U; Android 7.1.2; en; SM-N975F; Build/N2G48H;tt-ok/{str(random.randint(1,10**19))})',
        'language': 'AR'
    }
    signer.updateHeaders(headers)
    headers.update(sign(urlencode(params), "", "AadCFwpTyztA5j9L" + ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(9)), None, 1233))

    ticket = None
    for host in hosts:
        try:
            url = f'https://{host}/passport/account_lookup/email/'
            r = ss.post(url, params=params, headers=headers, timeout=15)
            
            data = r.json()
            #print(data)
            if data.get('data', {}).get('accounts'):
                ticket = data['data']['accounts'][0]['passport_ticket']
                break
        except:
            time.sleep(2)

    if not ticket:
        return None

    params["not_login_ticket"] = ticket
    params["type"] = "3737"

    for host in hosts:
        try:
            temp = ss.post('https://api.internal.temp-mail.io/api/v3/email/new').json()
            name = temp["email"]
            params["email"] = name

            headers.update(sign(urlencode(params), "", "AadCFwpTyztA5j9L" + ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(9)), None, 1233))
            url2 = f"https://{host}/passport/email/send_code"
            r2 = ss.post(url2, params=params, headers=headers, timeout=15)

            if r2.json().get("message") == "success":
                for _ in range(15):
                    time.sleep(5)
                    msgs = ss.get(f'https://api.internal.temp-mail.io/api/v3/email/{name}/messages').json()
                    if isinstance(msgs, list) and msgs:
                        tx = msgs[0].get("body_text", "")
                        #print(tx)
                        patterns = [
                            r"تم إنشاء هذا البريد الإلكتروني من أجل\s+([^\s]+)",
                            r"This email was created for\s+([^\s]+)",
                            r"created for\s+([^\s]+)",
                            r"@([A-Za-z0-9_.]+)\s+هو حسابك",
                            r"username\s*:\s*([^\s,]+)",
                            r"@([A-Za-z0-9_.]+)"
                        ]
                        for p in patterns:
                            m = re.search(p, tx)
                            if m:
                                return m.group(1)
                    
        except:
            time.sleep(3)

    return None
#print(email2user(input("Rmailllllllll :")))    
