import time
import argparse

import asyncio
import aiohttp

from rates import Rates
from money import Wallet
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

def parse_init_params():
    parser = argparse.ArgumentParser(description='Get initial parameters.')

    parser.add_argument('--period', action='store', dest='N', required=True,
                        help='period of updating the exchange rate, in minutes')
    parser.add_argument('--rub', action='store', dest='rub', type=float, required=True)
    parser.add_argument('--eur', action='store', dest='eur', type=float, required=True)
    parser.add_argument('--usd', action='store', dest='usd', type=float, required=True)
    parser.add_argument('--debug', action='store', dest='debug', type=str2bool, default=False)

    return parser.parse_args()


class Monitoring:
    args = []

    def __init__(self, currencies):
        self.args = vars(parse_init_params())

        self.rate = Rates()

        cash = {}
        for currency in currencies:
            if currency in self.args:
                cash[currency] = self.args[currency]
        self.wallet = Wallet(cash)

    def run(self):
        asyncio.run(self.run_tasks())

    async def run_tasks(self):
        asyncio.create_task(self.update_exchange_rate())
        asyncio.create_task(self.print_rate_and_purse())
        asyncio.create_task(self.run_web_server())

        await asyncio.Event().wait()

    async def update_exchange_rate(self):
        while True:
            self.rate.update()
            print(self.rate.get())
            await asyncio.sleep(5)

    async def print_rate_and_purse(self):
        while True:
            print(self.wallet.get())
            print()
            print(self.rate.get())
            print('sum: ...')
            await asyncio.sleep(7)

    async def run_web_server(self):
        app = aiohttp.web.Application()
        for route in routes:
            app.router.add_route(route[0], route[1], route[2], name=route[3])

        runner = aiohttp.web.AppRunner(app)
        await runner.setup()
        await aiohttp.web.TCPSite(runner).start()
