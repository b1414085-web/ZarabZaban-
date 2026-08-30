import requests,json,SignerPy,secrets,uuid,random,os,binascii,time,string,re
from hsopyt import Gorgon,Ladon,Argus,md5,urlencode
#os.system("pip install mustafatik --upgrade")
from mustafatik import mustafatik
os.system("clear")
def sign(params: str, payload: str or None = None, sec_device_id: str = '', cookie: str or None = None, aid: int = 1233, license_id: int = 1611921764, sdk_version_str: str = 'v05.00.06-ov-android', sdk_version: int = 167775296, platform: int = 0, unix: float = None):
        x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload != None else None
        if not unix: unix = time.time()

        return Gorgon(params, unix, payload, cookie).get_value() | {
            'content-length' : str(len(payload)),
            'x-ss-stub'      : x_ss_stub.upper(),
            'x-ladon'        : Ladon.encrypt(int(unix), license_id, aid),
            'x-argus'        : Argus.get_sign(params, x_ss_stub, int(unix),
                platform        = platform,
                aid             = aid,
                license_id      = license_id,
                sec_device_id   = sec_device_id,
                sdk_version     = sdk_version_str, 
                sdk_version_int = sdk_version
            )}
hosts=["api22-normal-c-alisg.tiktokv.com","api31-normal-useast2a.tiktokv.com","api2.musical.ly","api16-normal-c-useast1a.tiktokv.com","http://api16-normal-de.tiktokv.eu"]
def Rest(username):
	for hh in hosts:
		try:
				params = {'app_version': '36.5.5', 'ac': 'wifi', 'account_param': SignerPy.xor(username), 'aid': '1233', 'channel': "appstore", 'locale': 'en', 'mix_mode': '1', 'os': 'android', 'region': 'US', 'request_tag_from': 'h5', 'scene': '4', 'version_code': '360505'};tk=mustafatik();tk.updateParams(params)
				sess = requests.session()
				headers = {
				  'User-Agent': "com.zhiliaoapp.musically/2023708050 (Linux; U; Android 9; en_US; G011A; Build/PI;tt-ok/3.12.13.16)",};headers.update(sign(urlencode(params),"" ,"AadCFwpTyztA5j9L" + ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(9)), None, 1233));tk.updateHeaders(headers)
				
				response = sess.post(f"https://{hh}/passport/account_lookup/username/", headers=headers,params=params)
				#print(response.text)
				passport_ticket=response.json()["data"]["accounts"][0]["passport_ticket"]
				params['passport_ticket'] = passport_ticket
				
				
				
				#ـــــــــــــــــــــــــــــــــــــNumber 2 
				headers = {
				  'User-Agent': "com.zhiliaoapp.musically/2023708050 (Linux; U; Android 9; en_US; G011A; Build/PI;tt-ok/3.12.13.16)",};headers.update(sign(urlencode(params),"" ,"AadCFwpTyztA5j9L" + ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(9)), None, 1233));tk.updateHeaders(headers)
				response = sess.post(f"https://{hh}/passport/user/login_by_passport_ticket/", headers=headers,params=params)
				
				#—————#
				
				info = {"email": None, "phone": None}
				rest = response.headers.get('X-Tt-Verify-Idv-Decision-Conf')
				if rest:
				    k = json.loads(rest)
				    for item in k.get("extra", []):
				        val = item.get("info", "")
				        if not val:
				            continue
				        if "@" in val:
				            info["email"] = val
				        elif re.match(r"^\+?\d[\d\*\s-]*$", val):
				            info["phone"] = val
				           
				else:print("Problem")
				return info				
		except:pass
#print(Rest(input("Enter TikTok UserName  : ")))
