import aiohttp
import asyncio
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
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                    async with session.get(url) as resp:
                        print(f"[PW API] Attempt {attempt}, Status: {resp.status}")
                        data = await resp.json()
                        print(f"[PW API] Response: {data}")

                        if isinstance(data, dict):
                            token = data.get("token") or data.get("access_token") or data.get("data")
                            if token and isinstance(token, str):
                                return token.strip()
                        raise RuntimeError("Token not found in response")

            except Exception as e:
                last_error = e
                print(f"[PW API] Attempt {attempt} failed: {e}")
                await asyncio.sleep(1.5 * attempt)

        raise RuntimeError(f"PW API failed after {self.retries} attempts: {last_error}")
