import aiohttp
import asyncio
from pydantic import BaseModel
from aiofiles import open

class VKAccount(BaseModel):
    token: str

class AccountChecker:
    def __init__(self, account: VKAccount):
        self.account = account
    async def check_vk_account(self):
        async with aiohttp.ClientSession() as session:
            url = f"https://api.vk.com/method/users.get?access_token={self.account.token}&v=5.131"
            async with session.get(url) as response:
                if response.status == 200:
                    json_response = await response.json()
                    if 'error' in json_response:
                        return False
                    else:
                        return True
                else:
                    return False
    async def save_result(self, is_working: bool):
        result = 'working' if is_working else 'not_working'
        async with open(f"{result}.txt", mode='a') as file:
            await file.write(f"{self.account.token}\n")
async def main():
    async with open("tokens.txt", mode='r') as f:
        tokens = await f.readlines()
        accounts = [VKAccount(token=token.strip()) for token in tokens]
    checkers = [AccountChecker(account) for account in accounts]
    results = await asyncio.gather(*[checker.check_vk_account() for checker in checkers])
    for checker, result in zip(checkers, results):
        await checker.save_result(result)
if __name__ == '__main__':
    asyncio.run(main())
