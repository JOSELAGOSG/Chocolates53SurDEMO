from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Purchase)
admin.site.register(models.PurchaseItem)
admin.site.register(models.Freight)
admin.site.register(models.Box)
admin.site.register(models.Payment)
admin.site.register(models.Product)
admin.site.register(models.Brand)
admin.site.register(models.Provider)
admin.site.register(models.FreightCompany)