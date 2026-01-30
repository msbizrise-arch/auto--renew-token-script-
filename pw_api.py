import aiohttp
import asyncio

class PWTokenService:
    BASE_URL = "https://anonymouspwplayer-554b25895c1a.herokuapp.com/pw"

    @staticmethod
    async def renew_token(old_token: str) -> str:
        """
        Calls PW backend API and returns renewed token
        """
        async with aiohttp.ClientSession() as session:
            params = {"token": old_token}
            async with session.get(PWTokenService.BASE_URL, params=params) as resp:
                if resp.status != 200:
                    raise Exception("PW API Failed")

                data = await resp.json()
                # Assuming API returns {"token": "NEW_TOKEN"}
                return data.get("token", "INVALID_RESPONSE")
