import aiohttp
import json


class ApexApi:
    def __init__(self, pid, platform):
        self.pid = pid
        self.platform = platform
        self.data = self.get()
        self.username = ""

    async def get(self):
        api_key = "8f3f57203dfaeae9f1497c9ac8d10b4c"
        async with aiohttp.ClientSession(base_url="https://api.mozambiquehe.re") as session:
            async with session.get(f"/bridge?auth={api_key}&player={self.pid})&platform={self.platform}") as data:
                return json.loads(await data.text())
