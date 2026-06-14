from django.db import models

# Create your models here.

class Recipie(models.Model):
    recipie_name = models.CharField(max_length=100)
    description = models.TextField()

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()

class ReciepieItem(models.Model):
    recipie_name = models.ForeignKey(Recipie,on_delete=models.CASCADE)
    ingredient_name = models.ForeignKey(Ingredient,on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)