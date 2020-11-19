import json
from aiohttp import web
from money import Wallet


async def hello(request):
    return web.Response(text='Hello, world')

async def get_data(request):
    currency = request.match_info['currency']
    result = {
        currency: Wallet().get(currency)
    }
    return web.Response(text=json.dumps(result))

async def set_data(request):
    currency = request.match_info['currency']
    try:
        data = await request.json()
    except json.JSONDecodeError as e:
        print(e)
        data = '{}'

    text = currency + json.dumps(data)
    return web.Response(text=text)

async def modify_data(request):
    return web.Response(text='Hello, world')

routes = [
    ('GET', '/', hello, 'hello'),
    ('GET', '/{currency}/get', get_data, 'get'),
    ('POST', '/{currency}/set', set_data, 'set'),
    ('POST', '/modify', modify_data, 'modify'),
]
