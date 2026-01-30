import aiohttp
import asyncio
import time
from urllib.parse import quote_plus


BASE_API = "https://anonymouspwplayer-554b25895c1a.herokuapp.com/pw"


class PWTokenService:
    def __init__(self, timeout=20, retries=3):
        self.timeout = timeout
        self.retries = retries

    async def renew_token(self, raw_token: str) -> str:
        if not raw_token or "." not in raw_token:
            raise ValueError("Invalid token format")

        encoded_token = quote_plus(raw_token)
        url = f"{BASE_API}?token={encoded_token}"

        last_error = None

        for attempt in range(1, self.retries + 1):
            try:
                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as session:
                    async with session.get(url) as resp:
                        if resp.status != 200:
                            raise RuntimeError(f"HTTP {resp.status}")

                        data = await resp.json()

                        # expected strong validation
                        if isinstance(data, dict):
                            token = (
                                data.get("token")
                                or data.get("access_token")
                                or data.get("data")
                            )

                            if token and isinstance(token, str):
                                return token.strip()

                        raise RuntimeError("Token not found in response")

            except Exception as e:
                last_error = e
                await asyncio.sleep(1.2 * attempt)

        raise RuntimeError(f"PW API failed: {last_error}")
