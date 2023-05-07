import aiohttp
import json


class MLBBApi:
    def __init__(self, uid, zid):
        self.uid = uid
        self.zid = zid
        self.banners = "banners"
        self.hotBanners = "hot/banners"
        self.guideBanners = "guide/banners"
        # --- Videos ---
        self.videos = "videos"
        self.videosDetail = "videos/detail"
        # --- Creator Camp ---
        self.creatorCamp = "creatorcamp"
        self.creatorCampVideos = "creatorcamp/videos"
        self.creatorCampActivity = "creatorcamp/activity"
        # --- Sports ---
        self.sports = "sports"
        self.sportsBanners = "sports/banners"
        self.sportsdetails = "sports/detail"
        # --- Misc ---
        self.nationMatch = "nationMatch"
        self.paymentCountries = "payment/countries"
        self.homepage = "landing"
        self.skillList = "skillList"
        self.commonTerms = "commonTerms"
        self.strategies = "strategies"
        self.equipments = "equipments"
        self.news = "newsAndVideos"
        self.schedules = "schedules"
        self.matches = "matches"
        self.username = "user/name"

    async def get(self, endpoint):
        endpoint = "/api/free/games /mobilelegends/" + endpoint
        async with aiohttp.ClientSession(base_url="http://167.172.85.80") as session:
            async with session.get(f"{endpoint}?id={self.uid}&zoneID={self.zid}") as data:
                print(json.loads(await data.text()))
                return json.loads(await data.text())
