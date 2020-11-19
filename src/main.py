import time
import argparse

import asyncio
import aiohttp

from rates import Rates
from money import Purse
from routes import routes


def str2bool(value):
    if isinstance(value, bool):
        return value
    elif value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


parser = argparse.ArgumentParser(description='Get initial parameters.')

parser.add_argument('--period', action='store', dest='N', required=True,
                    help='period of updating the exchange rate, in minutes')
parser.add_argument('--rub', action='store', dest='rub', type=float, required=True)
parser.add_argument('--eur', action='store', dest='eur', type=float, required=True)
parser.add_argument('--usd', action='store', dest='usd', type=float, required=True)
parser.add_argument('--debug', action='store', dest='debug', type=str2bool, default=False)

args = parser.parse_args()

rate = Rates()

cash = {
    'rub': args.rub,
    'eur': args.eur,
    'usd': args.usd,
}
purse = Purse(cash)

async def get_exchange_rate():
    while True:
        rate.update()
        print(rate.get())
        await asyncio.sleep(5)


async def print_rate_and_purse():
    while True:
        print(purse.get())
        print()
        print(rate.get())
        print('sum: ...')
        await asyncio.sleep(7)


async def main():
    # create the application, as before
    app = aiohttp.web.Application()
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])

    # add some tasks into the current event loop
    asyncio.create_task(get_exchange_rate())
    asyncio.create_task(print_rate_and_purse())

    # set up the web server
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    await aiohttp.web.TCPSite(runner).start()

    # wait forever, running both the web server and the tasks
    await asyncio.Event().wait()

asyncio.run(main())
