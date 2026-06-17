from django.shortcuts import render,redirect
from frontmodules.models import Ingredient
from django.views import View
from django.http import JsonResponse


# Create your views here.

class IngredientListView(View):
    def get(self,req):
        ingredients = Ingredient.objects.all()
        return render(req,'ingredientlist.html',{'ingredients':ingredients})
    

def live_search(req):

    query = req.GET.get("q","").strip()
    ingredients = Ingredient.objects.filter(ingredient_name__istartswith = query)

    if not query:
        return JsonResponse([],safe=False)
    
    data = list(
        ingredients.values(
            "id",
            "ingredient_name"
        )
    )

    return JsonResponse(data,safe=False)