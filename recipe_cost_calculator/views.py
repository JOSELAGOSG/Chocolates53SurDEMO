from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import NonWarehouseProduct, Recipe, NonWarehouseIngredient , WarehouseIngredient

# NonWarehouseProduct CRUD Views

class NonWarehouseProductCreateView(CreateView):
    model = NonWarehouseProduct
    fields = '__all__'

class NonWarehouseProductListView(ListView):
    model = NonWarehouseProduct
    context_object_name = 'products'

class NonWarehouseProductDetailView(DetailView):
    model = NonWarehouseProduct
    context_object_name = 'product'

class NonWarehouseProductUpdateView(UpdateView):
    model = NonWarehouseProduct
    fields = '__all__'
    template_name_suffix = '_update_form'

class NonWarehouseProductDeleteView(DeleteView):
    model = NonWarehouseProduct
    context_object_name = 'product'
    success_url = reverse_lazy('recipes:non-wh-product-list')


# Recipe CRUD Views

class RecipeCreateView(CreateView):
    model = Recipe
    fields = '__all__'

class RecipeListView(ListView):
    model = Recipe
    context_object_name = 'recipes'

class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'

class RecipeUpdateView(UpdateView):
    model = Recipe
    template_name_suffix = '_update_form'

class RecipeDeleteView(DeleteView):
    model = Recipe
    context_object_name = 'recipe'
    success_url = reverse_lazy('recipes:recipe-list')


#WarehouseIngredient CRUD Views

class WarehouseIngredientCreateView(CreateView):
    model = WarehouseIngredient
    fields = ['product', 'quantity']

    def form_valid(self, form):
        recipe_pk = self.kwargs['recipe_pk']
        self.object = WarehouseIngredient.objects.create(
            recipe = Recipe.objects.get(pk=recipe_pk),
            product = form.cleaned_data['product'],
            quantity = form.cleaned_data['quantity']
        )
        return redirect(self.object.recipe.get_absolute_url())

class WarehouseIngredientListView(ListView):
    model = WarehouseIngredient
    context_object_name = 'ingredients'

class WarehouseIngredientDetailView(DetailView):
    model = WarehouseIngredient
    context_object_name = 'ingredient'

class WarehouseIngredientUpdateView(UpdateView):
    model = WarehouseIngredient
    template_name_suffix = '_update_form'

class WarehouseIngredientDeleteView(DeleteView):
    model = WarehouseIngredient
    context_object_name = 'ingredient'

    def get_success_url(self):
        recipe_pk = self.kwargs['recipe_pk']
        return reverse_lazy('recipes:recipe-detail', kwargs={'pk': recipe_pk})



#NonWarehouseIngredient CRUD Views

class NonWarehouseIngredientCreateView(CreateView):
    model = NonWarehouseIngredient
    fields = ['product', 'quantity']

    def form_valid(self, form):
        recipe_pk = self.kwargs['recipe_pk']
        self.object = NonWarehouseIngredient.objects.create(
            recipe = Recipe.objects.get(pk=recipe_pk),
            product = form.cleaned_data['product'],
            quantity = form.cleaned_data['quantity']
        )
        return redirect(self.object.recipe.get_absolute_url())

class NonWarehouseIngredientListView(ListView):
    model = NonWarehouseIngredient
    context_object_name = 'ingredients'

class NonWarehouseIngredientDetailView(DetailView):
    model = NonWarehouseIngredient
    context_object_name = 'ingredient'

class NonWarehouseIngredientUpdateView(UpdateView):
    model = NonWarehouseIngredient
    template_name_suffix = '_update_form'

class NonWarehouseIngredientDeleteView(DeleteView):
    model = NonWarehouseIngredient
    context_object_name = 'ingredient'
    #success_url
