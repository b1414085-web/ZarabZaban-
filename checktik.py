import requests,SignerPy,random,asyncio,aiohttp
sesf="data/GoodSessIons.txt"
sds = open(sesf, "r").read().splitlines()
async def checktiktok(email, session):
    for i in range(3):
        try:
            params = {
                "aid": "1233",
                "app_version": "37.8.8",
                "version_name": "37.8.8",
                "app_language": "en",
                'device_id': str(random.randint(1, 10**19)),
            }

            headers = {
                'User-Agent': 'com.zhiliaoapp.musically/2022509040 (Linux; U; Android 200; ar; TECNO CL8; Build/SP1A.210812.001; Cronet/TTNetVersion:ae513f3c 2022-08-08 QuicVersion:12a1d5c5 2022-06-27)',
                **SignerPy.sign(params=params, payload={'email': email}, version=4404, aid=1233),
                'Cookie': f'sid_tt={random.choice(sds)}'
            }

            async with session.post(
                "https://api22-normal-c-alisg.tiktokv.com/passport/email/bind_without_verify/",
                headers=headers,
                data={'email': email+"@gmail.com"},
                params=params
            ) as r:

                mustafa = await r.text()
                #print(mustafa)

                if 'Email is linked to another account. Unlink or try another email.' in mustafa:
                    return True
                elif 'Account is already linked' in mustafa:
                    return False
                elif 'Session expired' in mustafa:
                    return None

        except Exception as e:
            print(e)
            pass

async def main():
    try:
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*(checktiktok("vhjjkvjkgho", session) for i in range(5)))
    except Exception as e:
        print(e)
        pass

#asyncio.run(main())
