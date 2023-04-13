from django.db import models
from warehouse.models import Product
from django.urls import reverse
from decimal import Decimal

''' NonWarehouseProduct is a model for handling products that are not being handled in Warehouse app.
    (e.g. Butter, Suggar). These products might be added directly into the factory without previous registration'''

class NonWarehouseProduct(models.Model):
    name = models.CharField(max_length=30, null=False)
    price_per_un_of_measurement = models.IntegerField()
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipes:non-wh-product-detail', args=[self.pk])


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def get_wh_cost(self):
        cost = 0
        for ingredient in self.warehouse_ingredients.all():
            cost += ingredient.get_cost()
        return cost
    
    def get_non_wh_cost(self):
        cost = 0
        for ingredient in self.non_warehouse_ingredients.all():
            cost += ingredient.get_cost()
        return cost
    
    def get_cost(self):
        return self.get_wh_cost() + self.get_non_wh_cost()
    
    def get_absolute_url(self):
        return reverse('recipes:recipe-detail', args=[self.pk])

    def get_create_non_wh_ingredient_url(self):
        return reverse('recipes:non-wh-ingredient-create', args=[self.pk])
    
    def get_create_wh_ingredient_url(self):
        return reverse('recipes:wh-ingredient-create', args=[self.pk])

class WarehouseIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='warehouse_ingredients')
    '''product: foreign key to warehouse/product model. '''
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    
    def get_absolute_url(self):
        return reverse('recipes:wh-ingredient-detail', args=[self.pk])

    def get_cost(self):
        wh_product = Product.objects.get(pk=self.product.pk)
        product_highest_price_per_un_of_measurement = wh_product.get_highest_price_per_un_of_measurement()
        
        return self.quantity * Decimal(product_highest_price_per_un_of_measurement)

class NonWarehouseIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='non_warehouse_ingredients')
    product = models.ForeignKey(NonWarehouseProduct, on_delete=models.PROTECT, related_name='non_warehouse_ingredients')
    quantity = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)

    def get_cost(self):
        non_wh_product = NonWarehouseProduct.objects.get(pk=self.product.pk)
        cost = self.quantity * Decimal(non_wh_product.price_per_un_of_measurement)
        return cost

    def get_absolute_url(self):
        return reverse('recipes:non-wh-ingredient-detail', args=[self.pk])

