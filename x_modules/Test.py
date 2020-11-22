import aiohttp
import asyncio
import random
import re

async def check_response(content):
    # print("Contents check.....")
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
    # print(f'Started downloading {ip}')
    print("=", end='', flush=True)
    async with aiohttp.ClientSession() as session:
        try:
            path = "index.php"
            url = f"http://{ip}/{path}"
            async with session.post(url, timeout=timeout) as resp:
                # status = resp.status
                # if status == 200:
                #     print("200: OK")
                # if status == 301:
                #     print("301: Moved Permanently")
                # if status == 302:
                #     print("302: Moved Temporarily")
                # if status == 304:
                #     print("304: Not Modified")
                # if status == 307:
                #     print("307: Temporary Redirect")
                # if status == 400:
                #     print("400: Bad Request")
                # if status == 401:
                #     print("401: Unauthorized")
                # if status == 403:
                #     print("403: Forbidden")
                # if status == 404:
                #     print("404: Not Found")
                # if status == 405:
                #     print("405: Method Not Allowed")
                # if status == 410:
                #     print("410: Gone")
                # if status == 500:
                #     print("500: Internal Server Error")
                # if status == 502:
                #     print("502: Bad Gateway")
                # if status == 503:
                #     print("503: Service Unavailable")
                # if status == 504:
                #     print("504: Gateway Timeout")
                # if status == 550:
                #     print("550: Permission Denied")
                
                # headers = resp.headers
                # print(headers['Server'])
                # for header in headers:
                #     print(f"{header}: {headers[header]}\r\n")

                content = await resp.read()
                # print(f'Finished downloading {url}\nUsing delay {delay}')
                if await check_response(content):
                    # print("PASS! Content check good!")
                    return content
                else:
                    print("FAIL! Content check fail, restarting download...\n")
        except asyncio.TimeoutError as e:
            # print(f"FAIL! Timed out!")
            # print(f"Error: {e}\n")
            pass
        except aiohttp.client_exceptions.ClientConnectorError as e:
            # print(f"FAIL! Couldn't connect")
            # print(f"Error: {e}\n")
            pass
        except aiohttp.client_exceptions.ClientResponseError as e:
            # print(f"FAIL! Client response error")
            # print(f"Error: {e}\n")
            pass
        except Exception as e:
            # print(f"Uh oh. Something fucked up: {e}\n")
            pass