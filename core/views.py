from django.shortcuts import render
from currency.services import ExchangeRateService


# Create your views here.
def index(request):
    service = ExchangeRateService()
    rates = service.get_rates()
    print(rates)
    return render(request, 'core/index.html')
