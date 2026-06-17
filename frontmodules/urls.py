from django.urls import path
from frontmodules.views import *

urlpatterns = [
    path('ilist',IngredientListView.as_view(),name='ilist'),
    path('findrecipies',ViewRecipies.as_view(),name="viewrecipies"),
]