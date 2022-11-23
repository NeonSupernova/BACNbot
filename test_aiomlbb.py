import pytest

uid = 27635464
zid = 5009


async def test_banners():
    cli = aiomlbb.MLBBApi(uid, zid)
    data = await cli.get('banners')
    assert data['status'] == 'success'


async def test_hot_banners():
    cli = aiomlbb.MLBBApi(uid, zid)
    data = await cli.get('hotBanners')
    assert data['status'] == 'success'


async def test_guide_banners():
    cli = aiomlbb.MLBBApi(uid, zid)
    data = await cli.get('guideBanners')
    assert data['status'] == 'success'

