import asyncio
import aiohttp
import csv



class ValidationProxy:
    def __init__(self):
        self._url = 'https://httpbin.org/ip'

    def write_proxy(self, value: str) -> None:
        with open('valid_proxies.txt', 'a+') as file:
            file.seek(0)
            content = file.readlines()
            if f'{value}\n' not in content:
                file.write(value + '\n')
                file.flush()

    def total_proxies(self) -> int:
        with open('list_proxies.csv', 'r') as f:
            count_row = sum([1 for row in f])
        return count_row

    def get_proxies(self) -> list:
        with open('list_proxies.csv', 'r') as f:
            reader = csv.reader(f)
            all_proxies = [row[0] for row in reader]
        return all_proxies

    async def fetch(self, session, url: str, proxy: str, id_proxy: int) -> None:
        try:
            async with session.get(url=url, proxy=proxy, timeout=10) as response:
                json_response = await response.json()
                await asyncio.sleep(1)
                print(f'Proxy {id_proxy} - VALID')
                self.write_proxy(proxy)
        except:
            print(f'Proxy {id_proxy} - not valid')
            pass

    async def check_valid(self) -> None:
        async with aiohttp.ClientSession() as session:
            all_proxies = self.get_proxies()
            count = self.total_proxies()
            tasks = []
            for i, proxy in enumerate(all_proxies):
                if 'http://' not in proxy:
                    proxy = f'http://{proxy}'
                print(f'In progress {i}/{count}')
                tasks.append(self.fetch(session, self._url, proxy, i))
            await asyncio.gather(*tasks)

    def run(self):
        asyncio.run(self.check_valid())


validation = ValidationProxy()
validation.run()