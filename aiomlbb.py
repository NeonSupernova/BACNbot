import aiohttp
import json
from unsync import unsync


class MLBBApi:
    def __init__(self, uid, zid):
        # Endpoints
        self.ENDPOINTS = {
            "banners": "/api/free/games/mobilelegends/banners",
            "hotBanners": "/api/free/games/mobilelegends/hot/banners",
            "guideBanners": "/api/free/games/mobilelegends/guide/banners",
            "sportsBanners": "/api/free/games/mobilelegends/sports/banners",
            "videos": "/api/free/games/mobilelegends/videos",
            "videoDetail": "/api/free/games/mobilelegends/videos/detail",
            "creatorCamp": "/api/free/games/mobilelegends/creatorcamp",
            "creatorCampVideos": "/api/free/games/mobilelegends/creatorcamp/videos",
            "creatorCampActivity": "/api/free/games/mobilelegends/creatorcamp/activity",
            "sports": "/api/free/games/mobilelegends/sports",
            "sportDetails": "/api/free/games/mobilelegends/sports/detail",
            "nationMatch": "/api/free/games/mobilelegends/nationMatch",
            "paymentCountries": "/api/free/games/mobilelegends/payment/countries",
            "homepage": "/api/free/games/mobilelegends/landing",
            "skillList": "/api/free/games/mobilelegends/skillList",
            "commonTerms": "/api/free/games/mobilelegends/commonTerms",
            "strategies": "/api/free/games/mobilelegends/strategies",
            "equipments": "/api/free/games/mobilelegends/equipments",
            "news": "/api/free/games/mobilelegends/newsAndVideos",
            "schedules": "/api/free/games/mobilelegends/schedules",
            "matches": "/api/free/games/mobilelegends/matches",
            "username": "/api/free/games/mobilelegends/user/name",
        }
        self.UID = uid
        self.ZID = zid
        self.ENP = None
        self.status = None

    async def fetch(self, session):
        async with session.get(f"{self.ENP}?id={self.UID}&zoneID={self.ZID}") as resp:
            assert resp.status == 200
            return await resp.text()

    #@unsync
    async def get(self, endpoint):
        if endpoint in self.ENDPOINTS:
            self.ENP = self.ENDPOINTS[endpoint]
        else:
            self.status = False
            exit(1)
        async with aiohttp.ClientSession(base_url="http://167.172.85.80") as client:
            data = await self.fetch(client)
            return json.loads(data)
