from django.db import models
from django.utils import timezone


# Create your models here.
class ExchangeRateProvider(models.Model):
    name = models.CharField(max_length=20)
    api_url = models.URLField()


class ExchangeRate(models.Model):

    date = models.DateField(default=timezone.now)

    base_currency = models.CharField(max_length=20)
    currency = models.CharField(max_length=20)

    sale_rate = models.DecimalField(max_digits=10, decimal_places=4)
    buy_rate = models.DecimalField(max_digits=10, decimal_places=4)

    provider = models.ForeignKey(ExchangeRateProvider, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.base_currency}/{self.currency}"
