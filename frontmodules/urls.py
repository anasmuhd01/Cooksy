from django.urls import path
from frontmodules.views import *

urlpatterns = [
    path('ilist',IngredientListView.as_view(),name='ilist'),
    path('findrecipies',ViewRecipies.as_view(),name="viewrecipies"),
    path('buyrecipie/<int:id>',BuyRecipieView.as_view(),name='buyrecipie'),
    path('buy-all',BuyallFormView.as_view(),name='buy-all'),
    path('buy-selected',BuyselectedView.as_view(),name='buy-selected'),
    path('paymentverify',BuyallpaymentVerifyView.as_view(),name="paymentverify"),
]