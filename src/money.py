class Purse:
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
