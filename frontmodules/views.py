from django.shortcuts import render,redirect
from frontmodules.models import *
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.http import HttpResponse
# Create your views here.


RAZORPAY_KEY = "rzp_test_SxQtLPRLPQ08jd"
RAZORPAY_SECRET_KEY = "9Xk2z1fJQVK7X4MyVVxQVXO1"

class HomepageView(View):
    def get(self,req):
        return render(req,'homepage.html')

class IngredientListView(View):

    def get(self,req):

        ingredients = Ingredient.objects.all()
        data = req.GET.get('ingredients','')
        
        if not data:
            return render(req,'ingredientlist.html',{
                'ingredients':ingredients,'recipies':[],'user_input':[]
            })
        
        splitted_data = [i for i in data.split(',') if i]
        
        req.session['user_selected_items']=splitted_data

        recipies = ReciepieItem.objects.filter(ingredient_id__in = splitted_data)

        match_count ={}
        for item in recipies:
            recipie_id = item.recipie.id
            if recipie_id in match_count:
                match_count[recipie_id] += 1
            else:
                match_count[recipie_id] = 1
        
        matches = []
        matched_recipies_count = sorted(match_count.items(),key=lambda x:x[1],reverse=True)
        for recipie_id, match in matched_recipies_count:
            recipie_item = Recipie.objects.get(id=recipie_id)
            matches.append(recipie_item)

        messages.error(req,"Please Select Atleast One Ingredient")
        return render(req,'ingredientlist.html',{'ingredients':ingredients,'recipies':matches,'user_input':splitted_data})
 
    def post(self,req):
        data = req.POST.get('selected-ingredients','').strip()
        if not data:
            messages.error(req,'please select atleast one ingredients')
            return redirect('ilist')
        
        splitted_data = [i for i in data.split(',') if i]
        return redirect(
            f"{reverse('ilist')}?ingredients={','.join(splitted_data)}"
        )

    

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
        first_item = ingredients.first()
        recipie_name = first_item.recipie if first_item else None
        # print(ingredients)
        
        """
the all ingredient id of the recipie are in this i.ingredient.id so using req.session this can be passed and used
        """
        print(req.session.get("user selected:",selected))
        print("all ingredients ids")

        all_ingredients_id = list(
            ingredients.values_list('ingredient_id',flat=True)
        )
        req.session['all_ingredients'] = all_ingredients_id
       
        return render(req,'buyrecipie.html',{'ingredients':ingredients,'user_selected':user_selected_ingredients,'recipie_name':recipie_name})

@method_decorator(never_cache,name='dispatch')   
class BuyallFormView(View):
    def get(self,req):
        

        all_ingredients = req.session.get('all_ingredients',[])
        # print('all ingredient',all_ingredients)
        qs = Ingredient.objects.filter(id__in = all_ingredients)
        selected = Ingredient.objects.filter(id__in = all_ingredients)

        total_price = 0
        for i in selected:
            total_price += i.price
        print(total_price)
        
        client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET_KEY))

        data = { "amount": total_price*100, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data) 
        payment_id = payment.get('id')
        print(payment.get('id'))

        order = Order.objects.create(razr_pay_id=payment_id)
        # instead of looping and adding item set method is better it adds all in single query
        order.ingredient_object.set(qs)

        return render(req,'buyallform.html',{'all_ingredients':selected,'payment':payment,'razorpay_key':RAZORPAY_KEY,'total_price':total_price})
    
    

    def post(self,req):
        """
        on the model data already created by order in the get request add this user details 
        fethed from here then redirect to the RAZOR PAY PAGE 
        """
        print(req.POST)
        
        return render(req,'payment.html')

@method_decorator([csrf_exempt,never_cache],name='dispatch')
class BuyallpaymentVerifyView(View):
    
    def post(self,req): 
        """
        make two post req to handle the form data then checkout

        """
        
        print(req.POST.get('razorpay_order_id'))
        client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET_KEY))
        try:
            client.utility.verify_payment_signature(req.POST)
            razr_pay_id = req.POST.get('razorpay_order_id')  
            order = Order.objects.get(razr_pay_id=razr_pay_id)
            order.is_paid = True
            order.save()
        except:
            print('Failed')

        return redirect('home')
        
    
class BuyselectedView(View):
    def get(self,req):
        selected = req.session.get('user_selected_items')
        
        ingredients = Ingredient.objects.filter(id__in = selected)
        return render(req,'buyselectedform.html',{'selected_ingredients':ingredients})