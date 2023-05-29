import datetime

from django.shortcuts import render
from currency.services import ProviderService, ExchangeRateService


# Create your views here.
def index(request):
    providers_data = [
        {'name': 'Privatbank', 'api_url': 'https://api.privatbank.ua/p24api/exchange_rates'}
    ]
    start_date = datetime.datetime(2023, 1, 1)
    end_date = datetime.datetime.now()

    for data in providers_data:
        provider_service = ProviderService(name=data['name'], api_url=data['api_url'])
        service = ExchangeRateService(provider=provider_service.create_provider(),
                                      start_date=start_date,
                                      end_date=end_date)
        rates = service.get_rates()
        print(rates)
    return render(request, 'core/index.html')
