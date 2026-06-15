from django.shortcuts import render,redirect
from frontmodules.models import Ingredient
from django.views import View


# Create your views here.

class IngredientListView(View):
    def get(self,req):
        ingredients = Ingredient.objects.all()
        return render(req,'ingredientlist.html',{'ingredients':ingredients})
