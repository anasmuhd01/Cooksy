from django.shortcuts import render,redirect
from frontmodules.models import *
from django.views import View
from django.http import JsonResponse


# Create your views here.

class IngredientListView(View):

    def get(self,req):
        ingredients = Ingredient.objects.all()
        return render(req,'ingredientlist.html',{'ingredients':ingredients})
    
    def post(self,req):
        ingredients = Ingredient.objects.all()

        #print("id of the ingredient is :",req.POST.get('selected-ingredients'))

        data = req.POST.get('selected-ingredients')

        splited_data = data.split(',')

        # to passs the values as iterable use the below method 
        # using field lookups
        
        recipies = ReciepieItem.objects.filter(ingredient__id__in = splited_data)
        match_count = {}
        
        for i in recipies:
            recipie_id = i.recipie.id
            if recipie_id in match_count:
                match_count[recipie_id] += 1
            else:
                match_count[recipie_id] = 1

        """
        -python sort by first item in each tuple which is RECIPIE_ID we need to sort by 
        MATCH_COUNT so key = lambda x:x[1]
        -without reverse = True smallest count first so to make it correct order
        eg: (4, 1), (3, 3)]
        with reverse = True
        eg: [(3, 3), (4, 1)]
        """
        matches = []
        matched_recipies_count = (sorted(match_count.items(),key=lambda x:x[1],reverse=True))
        for recipie_id, match in matched_recipies_count:
            recipie_item = Recipie.objects.get(id=recipie_id)
            # print(recipie_item.recipie_name)
            matches.append(recipie_item)
        req.session['user_selected_items']=splited_data
        
        return render(req,'ingredientlist.html',{'recipies':matches,'ingredients':ingredients,'user_input':splited_data})
    

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
    
class BuyRecipieView(View):
    
    def get(self,req,**kwargs):
        selected = req.session.get('user_selected_items')
        

        user_selected_ingredients = Ingredient.objects.filter(id__in = selected)
       
        ingredients = ReciepieItem.objects.filter(recipie__id = kwargs.get('id'))

        #takes the first item of the model with first then use what item
        recipie_name = ingredients.first().recipie
        # print(ingredients)
        
        """
the all ingredient id of the recipie are in this i.ingredient.id so using req.session this can be passed and used
        """
        for i in ingredients:
            print(i.ingredient.id)
        # {'recipieitem':recipieitem}
        return render(req,'buyrecipie.html',{'ingredients':ingredients,'user_selected':user_selected_ingredients,'recipie_name':recipie_name})