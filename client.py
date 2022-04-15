import aiohttp
import asyncio


HOST = 'http://127.0.0.1:8080'


async def main():
    async with aiohttp.ClientSession() as session:
        # async with session.post(f'{HOST}/ads/',
        #                         json={'description': 'новый', 'header': 'продам велосипед', 'owner': 'петя'}) as response:
        #     resp = await response.json()
        #     print(resp)
        # async with session.get(f'{HOST}/ads/6') as resp:
        #     print(await resp.json())
        async with session.delete(f'{HOST}/ads/2') as resp:
            print(await resp.json())

asyncio.run(main())
