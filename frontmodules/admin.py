from django.contrib import admin
from frontmodules.models import *

# Register your models here.

admin.site.register(Recipie)
admin.site.register(Ingredient)
admin.site.register(ReciepieItem)
from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "is_paid",
        "created_at",
        "get_ingredients",
    )

    readonly_fields = ("get_ingredients",)
    exclude = ("ingredient_object",)

    def get_ingredients(self, obj):
        return ", ".join(
            ingredient.ingredient_name for ingredient in obj.ingredient_object.all()
        )

    get_ingredients.short_description = "Ingredients"