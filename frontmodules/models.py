from django.db import models

# Create your models here.

class Recipie(models.Model):
    recipie_name = models.CharField(max_length=100)
    description = models.TextField()
    # recipie_img = models.ImageField(upload_to='recicipie_images',null=True)

    # dunder method
    def __str__(self):
        return self.recipie_name

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='ingredient_image',null=True)

    # dunder method which called when python neeeds a string to be represented
    def __str__(self):
        return self.ingredient_name

class ReciepieItem(models.Model):
    recipie = models.ForeignKey(Recipie,on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient,on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)

    # dunder method
    def __str__(self):
        return f"{self.recipie.recipie_name}-{self.ingredient.ingredient_name}"
    

class Order(models.Model):
    ingredient_object = models.ManyToManyField(Ingredient)
    is_paid = models.BooleanField(default=False)
    razr_pay_id = models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100,blank=True)
    customer_email = models.CharField(max_length=100,blank=True)
    customer_phone = models.CharField(max_length=10,blank=True)
    customer_address = models.TextField(blank=True)
    
