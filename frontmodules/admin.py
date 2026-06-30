from django.contrib import admin
from frontmodules.models import *

# Register your models here.

admin.site.register(Recipie)
admin.site.register(Ingredient)
admin.site.register(ReciepieItem)
admin.site.register(Order)