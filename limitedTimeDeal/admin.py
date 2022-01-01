from django.contrib import admin
from limitedTimeDeal import models

# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.Deal)
admin.site.register(models.ClaimDeal)
