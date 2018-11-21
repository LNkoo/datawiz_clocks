from django.contrib import admin

from core import models

admin.site.register((
    models.Department, models.GroupOfProducts, models.Product,
    models.Worker, models.Courier, models.Characteristic, models.Consumer,
    models.Basket,
))
