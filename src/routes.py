import json
from aiohttp import web
from money import Wallet
from rates import Rates


async def hello(request):
    return web.Response(text='Hello, world')

async def get_amount(request):
    text = ''
    cash = Wallet().get()

    for currency in cash:
        text += '{}: {}\n'.format(currency, cash[currency])
    text += '\n'
    for currency in cash:
        if currency.lower() != 'rub':
            text += 'rub-{}: {}\n'.format(currency.lower(), Rates().get(currency))
        else:
            text += 'usd-eur: {}\n'.format(Rates().get('eur') / Rates().get('usd'))
    text += '\n'
    text += 'sum:'
    for currency in cash:
        text += ' {} {} /'.format(currency, Wallet().get_sum_in_currency(currency))

    return web.Response(text=text)

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
