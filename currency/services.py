import requests


class ExchangeRateService:
    CURRENCIES = ['GBP', 'USD', 'CHF', 'EUR']

    def get_rates(self):
        url = "https://api.privatbank.ua/p24api/exchange_rates"

        params = {
            'date': '14.05.2023'
        }

        response = requests.get(url, params=params)
        data = response.json()
        rates = data['exchangeRate']
        currency_rates = []
        base_currency = data['baseCurrencyLit']
        date = data['date']
        for r in rates:
            if r['currency'] not in self.CURRENCIES:
                continue
            currency_rates.append(
                {
                    'base_currency': base_currency,
                    'currency': r['currency'],
                    'date': date,
                    'sale_rate': r['saleRate'],
                    'buy_rate': r['purchaseRate']
                }
            )
        return currency_rates

