import concurrent
from concurrent.futures import ThreadPoolExecutor

import requests
from datetime import datetime, timedelta

from config.settings import MAX_WORKERS
from currency.models import ExchangeRateProvider, ExchangeRate


class ProviderService:
    def __init__(self, name, api_url):
        self.name = name
        self.api_url = api_url

    def create_provider(self):

        if ExchangeRateProvider.objects.filter(name=self.name, api_url=self.api_url).exists():
            print(f"Provider {self.name} is already exists")
            provider = ExchangeRateProvider.objects.get(name=self.name, api_url=self.api_url)
        else:
            provider = ExchangeRateProvider(name=self.name, api_url=self.api_url)
            provider.save()
            print(f"Provider {self.name} was successfully created")
        return provider


class ExchangeRateService:

    CURRENCIES = ['GBP', 'USD', 'CHF', 'EUR']

    def __init__(self, provider, start_date, end_date):
        self.provider = provider
        self.start_date = start_date
        self.end_date = end_date

    def get_rate(self, date):

        params = {
            'date': date.strftime('%d.%m.%Y')
        }

        response = requests.get(self.provider.api_url, params=params)
        data = response.json()
        rates = data['exchangeRate']
        currency_rates = []
        base_currency = data['baseCurrencyLit']
        date = data['date']
        for r in rates:
            if r['currency'] not in self.CURRENCIES:
                continue
            currency_rate = {
                    'base_currency': base_currency,
                    'currency': r['currency'],
                    'date': date,
                    'sale_rate': r['saleRate'],
                    'buy_rate': r['purchaseRate']
                }

            currency_rates.append(currency_rate)
            exchange_rate = ExchangeRate(date=datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d'),
                                         base_currency=base_currency, currency=r['currency'],
                                         sale_rate=r['saleRate'], buy_rate=r['purchaseRate'], provider=self.provider
                                         )
            exchange_rate.save()

        return currency_rates

    def get_rates(self):

        dates = [self.start_date + timedelta(days=i) for i in range((self.end_date - self.start_date).days + 1)]
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(self.get_rate, date=date) for date in dates]

            results = []
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        return results
