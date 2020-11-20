import json
from aiohttp import web
from money import Wallet, get_wallet_statement


async def hello(request):
    return web.Response(text='Hello, world')

async def get_amount(request):
    return web.Response(text=get_wallet_statement())

async def get_currency(request):
    currency = request.match_info['currency']
    return web.Response(text=str(Wallet().get(currency)))

async def set_currency(request):
    try:
        data = await request.json()
    except json.JSONDecodeError:
        data = {}

    result = Wallet().set(data)

    return web.Response(text=str(result))

async def modify_wallet(request):
    try:
        data = await request.json()
    except json.JSONDecodeError:
        data = {}

    result = Wallet().modify(data)

    return web.Response(text=str(result))


routes = [
    ('GET', '/', hello, 'hello'),
    ('GET', '/amount/get', get_amount, 'get_amount'),
    ('GET', r'/{currency:[a-z]{3}}/get', get_currency, 'get_currency'),
    ('POST', '/amount/set', set_currency, 'set_currency'),
    ('POST', '/modify', modify_wallet, 'modify_wallet'),
]
