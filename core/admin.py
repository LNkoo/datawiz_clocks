from django.contrib import admin

from core.models import Department, GroupOfProducts, Product, Courier, Worker, Characteristic

admin.site.register(Department)
admin.site.register(GroupOfProducts)
admin.site.register(Product)
admin.site.register(Worker)
admin.site.register(Courier)
admin.site.register(Characteristic)