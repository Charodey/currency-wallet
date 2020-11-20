from metasingleton import MetaSingleton
from rates import Rates


def get_wallet_statement():
    cash = Wallet().get()

    text = ''
    for currency in cash:
        text += '{}: {}\n'.format(currency, cash[currency])
    text += '\n'
    for currency in cash:
        if currency.lower() != 'rub':
            text += 'rub-{}: {}\n'.format(currency.lower(), Rates().get(currency))
        else:
            text += 'usd-eur: {}\n'.format(get_rate_ratio(Rates().get('eur'), Rates().get('usd')))
    text += '\n'
    text += 'sum:'
    for currency in cash:
        text += ' {} {} /'.format(currency, get_sum_in_currency(currency))

    return text[:-2]

def get_sum_in_currency(currency):
    amount = 0
    cash = Wallet().get()
    for curr in cash:
        amount += cash[curr] * (1 if curr == currency else get_rate_ratio(Rates().get(curr), Rates().get(currency)))

    return amount

def get_rate_ratio(value1, value2):
    if value1 is None:
        value1 = 1
    if value2 is None:
        value2 = 1

    return value1 / value2


class Wallet(metaclass=MetaSingleton):
    __allow_credit = True
    __cash = {
        'RUB': 0,
        'EUR': 0,
        'USD': 0,
    }

    def __init__(self, cash=None, allow_credit=True):
        if cash:
            self.set(cash)
        self.__allow_credit = allow_credit

    def get(self, currency=None):
        if currency:
            return self.__cash[currency.upper()] if currency.upper() in self.__cash else None

        return self.__cash

    def set(self, cash):
        if not self.__allow_credit:
            for currency in cash:
                if cash[currency] < 0:
                    return False

        for currency in cash:
            self.__cash[currency.upper()] = cash[currency]

        return True

    def modify(self, cash):
        if not self.__allow_credit:
            for currency in cash:
                if self.__cash[currency.upper()] + cash[currency] < 0:
                    return False

        for currency in cash:
            self.__cash[currency.upper()] += cash[currency]

        return True
