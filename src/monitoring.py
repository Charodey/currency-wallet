from abc import ABC
import time
import argparse
import sys

import asyncio
import aiohttp
import logging

from rates import Rates
from money import Wallet, get_wallet_statement
from web import routes


logger = logging.getLogger('CurrencyWallet')


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

def set_logger_options(is_debug=False):
    console_output_handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(console_output_handler)
    logger.setLevel(logging.DEBUG if is_debug else logging.INFO)


class Monitoring(ABC):
    def __init__(self, currencies):
        self.args = vars(parse_init_params())
        set_logger_options(self.args['debug'])
        logger.info('Starting app ...')

        self.rate = Rates(['EUR', 'USD'])

        cash = {}
        for currency in currencies:
            if currency in self.args:
                cash[currency] = self.args[currency]
        self.wallet = Wallet(cash)

    def run(self):
        asyncio.run(self.run_tasks())

    async def run_tasks(self):
        task_methods = [method for method in dir(self) if method.find('task_') == 0]
        for method in task_methods:
            asyncio.create_task(getattr(self, method)())

        await asyncio.Event().wait()


class MyMonitoring(Monitoring):
    async def task_update_exchange_rate(self):
        while True:
            self.rate.update()
            await asyncio.sleep(5)

    async def task_print_amount_info(self):
        amount_info = {}
        while True:
            await asyncio.sleep(60)
            new_amount_info = get_wallet_statement()
            if amount_info != new_amount_info:
                amount_info = new_amount_info
                logger.info('\nAmount info:\n%s\n', amount_info)

    async def task_run_web_server(self):
        app = aiohttp.web.Application()
        for route in routes:
            app.router.add_route(route[0], route[1], route[2], name=route[3])

        runner = aiohttp.web.AppRunner(app)
        await runner.setup()
        await aiohttp.web.TCPSite(runner).start()
