from django.shortcuts import render,redirect
from frontmodules.models import Ingredient
from django.views import View
from django.http import JsonResponse


# Create your views here.

class IngredientListView(View):

    def get(self,req):
        ingredients = Ingredient.objects.all()
        return render(req,'ingredientlist.html',{'ingredients':ingredients})
    
    def post(self,req):
        data = req.POST.get('selected-ingredients')
        splited_data = data.split(',')

        # for i in splited_data:
           
        #     selected_items = Ingredient.objects.get(id=i)
        # to passs the values as iterable use the below method 
        # using field lookups
        selected_items = Ingredient.objects.filter(id__in=splited_data)
        

         
        return render(req,'viewrecipies.html',{'selecteditems':selected_items})
    

    
    

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


class ViewRecipies(View):

    def get(self,req):
        return render(req,'viewrecipies.html')