import json
import requests
import logging
from metasingleton import MetaSingleton
import monitoring


class Rates(metaclass=MetaSingleton):
    __URL = 'https://www.cbr-xml-daily.ru/daily_json.js'

    __currency = {}

    def __init__(self, currency=None):
        if currency:
            for key in currency:
                self.__currency[key.upper()] = None

    def __requests(self):
        monitoring.logger.debug('rates request: %s', self.__URL)
        response = requests.get(self.__URL)
        monitoring.logger.debug('rates response: %s', response.text)

        try:
            return response.json()
        except json.JSONDecodeError:
            monitoring.logger.error('Ошибка получения курса валют')

    def update(self):
        data = self.__requests()

        for currency in self.__currency:
            self.__currency[currency] = data['Valute'][currency]['Value']

        if data and monitoring.logger.getEffectiveLevel() != logging.DEBUG:
            monitoring.logger.info('Успешное получение данных о курсах валют')
            monitoring.logger.info(self.__currency)

    def get(self, currency=None):
        if currency:
            return self.__currency[currency.upper()] if currency.upper() in self.__currency else None

        return self.__currency
