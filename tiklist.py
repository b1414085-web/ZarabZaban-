import asyncio
import aiohttp
import random
import time
from urllib.parse import urlencode
import SignerPy
from hsopyt import Gorgon, Argus, Ladon

OUTPUT_FILE = "data/MustafaList.txt"
CONCURRENCY = 50

visited = set()
ulist = []
visited_lock = asyncio.Lock()
ulist_lock = asyncio.Lock()
file_lock = asyncio.Lock()
number = 0
counter_lock = asyncio.Lock()

def generate_tiktok_headers(params, data_str=None, cookie_str=None):
    ts = int(time.time())
    ticket = ts * 1000
    query = urlencode(params)
    gorgon_obj = Gorgon(params=query, unix=ts, data=data_str, cookies=cookie_str)
    gorgon_data = gorgon_obj.get_value()
    try:
        x_argus = Argus.get_sign(queryhash=query, data=data_str, timestamp=ts, aid=int(params.get("aid", 1340)))
    except Exception:
        x_argus = ""
    try:
        x_ladon = Ladon.encrypt(ts, "1611921764", int(params.get("aid", 1233)))
    except Exception:
        x_ladon = ""
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookie_str if cookie_str else '',
        'User-Agent': 'com.zhiliaoapp.musically.go/350302 (Linux; U; Android 12; en_US; TECNO CL6; Build/AP3A.240905.015.A2;tt-ok/3.12.13.21-ul)',
        'sdk-version': '2',
        'x-argus': x_argus,
        'x-gorgon': gorgon_data.get("x-gorgon"),
        'x-khronos': str(ts),
        'x-ladon': x_ladon,
        'x-ss-req-ticket': str(ticket)
    }
    return headers

async def append_to_file(username: str):
    async with file_lock:
        await asyncio.to_thread(open(OUTPUT_FILE, "a").write, username + "\n")

async def parse_profile_html(html_text: str):
    try:
        user_id = html_text.split('"id":"', 1)[1].split('"', 1)[0]
    except Exception:
        user_id = None
    try:
        sec_uid = html_text.split('"secUid":"', 1)[1].split('"', 1)[0]
    except Exception:
        sec_uid = None
    return user_id, sec_uid

async def fetch_followers(session: aiohttp.ClientSession, username: str):
    try:
        async with session.get(f"https://www.tiktok.com/@{username}", timeout=15) as r:
            html = await r.text()
    except Exception:
        return []
    user_id, sec_uid = await parse_profile_html(html)
    if not user_id or not sec_uid:
        return []
    params = {
        "user_id": user_id,
        "count": "50",
        "page_token": "",
        "source_type": "4",
        "sec_user_id": sec_uid,
        "version_name": "40.6.0.3",
        "aid": "1340",
    }
    try:
        signer = await asyncio.to_thread(SignerPy.get, params=params.copy())
        params.update(signer)
    except Exception:
        pass
    cookie_str = "sessionid=1a70e142cce1b91248a39b257a66add0"
    headers = await asyncio.to_thread(generate_tiktok_headers, params, None, cookie_str)
    try:
        async with session.get(
            "https://api16-normal-c-alisg.tiktokv.com/lite/v2/relation/follower/list/",
            params=params,
            headers=headers,
            timeout=15
        ) as resp:
            data = await resp.json()
    except Exception:
        pass
        return []
    followers = []
    for u in data.get("followers", []):
        unique_id = u.get("unique_id")
        if unique_id:
            followers.append(unique_id)
    return followers

async def worker(worker_id: int, queue: asyncio.Queue, session: aiohttp.ClientSession):
    global number
    while True:
        username = await queue.get()
        try:
            async with visited_lock:
                if username in visited:
                    queue.task_done()
                    continue
                visited.add(username)
            followers = await fetch_followers(session, username)
            async with ulist_lock:
                new_users = [u for u in followers if u not in ulist]
                ulist.extend(new_users)
            for uname in new_users:
                async with counter_lock:
                    number += 1
                    print(f"<{uname}> ~~ [{number}]")
                await append_to_file(uname)
            async with ulist_lock:
                if ulist:
                    next_user = random.choice(ulist)
                    await queue.put(next_user)
        except Exception:
            pass
        finally:
            queue.task_done()

async def main(start_user):
 try:
    queue = asyncio.Queue()
    await queue.put(start_user)
    timeout = aiohttp.ClientTimeout(total=30)
    connector = aiohttp.TCPConnector(limit=0)
    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        workers = [asyncio.create_task(worker(i + 1, queue, session)) for i in range(CONCURRENCY)]
        await asyncio.gather(*workers)
 except:pass
async def GetList(start_user):
    try:
        await main(start_user)
    except Exception as e:
        pass
        print(e)
    return ulist
    
async def mainGg(): 
	#while 1: 
	rli=open("data/MustafaList.txt","r").readlines()
	if rli:
		while 1:
			user=random.choice(rli)
			await GetList(user)
	elif not rli:
			user=input("Enter User : ")
			await GetList(user)
asyncio.run(mainGg())
