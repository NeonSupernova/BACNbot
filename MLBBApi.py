import aiohttp
import json


class MLBBApi:
    def __init__(self, uid, zid):
        self.uid = uid
        self.zid = zid
        self.banners = self.get("/api/free/games/mobilelegends/banners")
        self.hotBanners = self.get("/api/free/games/mobilelegends/hot/banners")
        self.guideBanners = self.get("/api/free/games/mobilelegends/guide/banners")
        self.sportsBanners = self.get("/api/free/games/mobilelegends/sports/banners")
        self.videos = self.get("/api/free/games/mobilelegends/videos")
        self.videoDetail = self.get("/api/free/games/mobilelegends/videos/detail")
        self.creatorCamp = self.get("/api/free/games/mobilelegends/creatorcamp")
        self.creatorCampVideos = self.get("/api/free/games/mobilelegends/creatorcamp/videos")
        self.creatorCampActivity = self.get("/api/free/games/mobilelegends/creatorcamp/activity")
        self.sports = self.get("/api/free/games/mobilelegends/sports")
        self.sportDetails = self.get("/api/free/games/mobilelegends/sports/detail")
        self.nationMatch = self.get("/api/free/games/mobilelegends/nationMatch")
        self.paymentCountries = self.get("/api/free/games/mobilelegends/payment/countries")
        self.homepage = self.get("/api/free/games/mobilelegends/landing")
        self.skillList = self.get("/api/free/games/mobilelegends/skillList")
        self.commonTerms = self.get("/api/free/games/mobilelegends/commonTerms")
        self.strategies = self.get("/api/free/games/mobilelegends/strategies")
        self.equipments = self.get("/api/free/games/mobilelegends/equipments")
        self.news = self.get("/api/free/games/mobilelegends/newsAndVideos")
        self.schedules = self.get("/api/free/games/mobilelegends/schedules")
        self.matches = self.get("/api/free/games/mobilelegends/matches")
        self.username = self.get("/api/free/games/mobilelegends/user/name")

    async def get(self, endpoint):
        async with aiohttp.ClientSession(base_url="http://167.172.85.80") as session:
            async with session.get(f"{endpoint}?id={self.uid}&zoneID={self.zid}") as data:
                print(json.loads(await data.text()))
                return json.loads(await data.text())
