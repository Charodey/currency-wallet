import json
import requests


class Rates:
    __URL = 'https://www.cbr-xml-daily.ru/daily_json.js'

    __currency = {}

    def __init__(self, currency=['EUR', 'USD']):
        for key in currency:
            self.__currency[key.upper()] = None

    def __requests(self):
        response = requests.get(self.__URL)
        try:
            return response.json()
        except json.JSONDecodeError:
            raise 'Ошибка получения курса валют'

    def update(self):
        data = self.__requests()

        for currency in self.__currency:
            self.__currency[currency] = data['Valute'][currency]['Value']

    def get(self, currency=None):
        if not currency:
            return self.__currency
