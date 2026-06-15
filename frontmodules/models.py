from django.db import models

# Create your models here.

class Recipie(models.Model):
    recipie_name = models.CharField(max_length=100)
    description = models.TextField()
    recipie_img = models.ImageField(upload_to='recicipie_images')

    def __str__(self):
        return self.recipie_name

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.ingredient_name

class ReciepieItem(models.Model):
    recipie = models.ForeignKey(Recipie,on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient,on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.recipie.recipie_name}-{self.ingredient.ingredient_name}"