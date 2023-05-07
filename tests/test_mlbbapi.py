from BACNbot.utils import MLBBApi
uid = 27635464
zid = 5009


async def test_banners():
    cli = MLBBApi(uid, zid)
    data = await cli.get(cli.banners)
    assert data['status'] == 'success'


async def test_hot_banners():
    cli = MLBBApi(uid, zid)
    data = await cli.get(cli.hotBanners)
    assert data['status'] == 'success'


async def test_guide_banners():
    cli = MLBBApi(uid, zid)
    data = await cli.get(cli.guideBanners)
    assert data['status'] == 'success'
    
    
async def test_sports_banners():
    cli = MLBBApi(uid, zid)
    data = await cli.get(cli.sportsBanners)
    assert data['status'] == 'success'
