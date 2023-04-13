from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'recipes'

urlpatterns = [
    # Recipe CRUD
    path('', login_required(views.RecipeListView.as_view()), name='recipe-list'),
    path('create/', login_required(views.RecipeCreateView.as_view()), name='recipe-create'),
    path('<int:pk>/', login_required(views.RecipeDetailView.as_view( )), name='recipe-detail'),
    path('<int:pk>/update/', login_required(views.RecipeUpdateView.as_view()), name='recipe-update'),
    path('<int:pk>/delete/', login_required(views.RecipeDeleteView.as_view()), name='recipe-delete'),
    
    # WarehouseIngredient CRUD
    path('<int:recipe_pk>/wh-ingredient/create/', login_required(views.WarehouseIngredientCreateView.as_view()), name='wh-ingredient-create'),
    path('<int:recipe_pk>/wh-ingredient/<int:ingredient_pk>/', login_required(views.WarehouseIngredientDetailView.as_view()), name='wh-ingredient-detail'),
    path('<int:recipe_pk>/wh-ingredient/<int:ingredient_pk>/delete/', login_required(views.WarehouseIngredientDeleteView.as_view()), name='wh-ingredient-delete'),
    path('<int:recipe_pk>/wh-ingredient/<int:ingredient_pk>/update/', login_required(views.WarehouseIngredientUpdateView.as_view()), name='wh-ingredient-update'),
    path('<int:recipe_pk>/wh-ingredient/', login_required(views.WarehouseIngredientListView.as_view()), name='wh-ingredient-list'),

    # NonWarehouseIngredient CRUD
    path('<int:recipe_pk>/non-wh-ingredient/create', login_required(views.NonWarehouseIngredientCreateView.as_view()), name='non-wh-ingredient-create'),
    path('<int:recipe_pk>/non-wh-ingredient/<int:ingredient_pk>/', login_required(views.NonWarehouseIngredientDetailView.as_view()), name='non-wh-ingedient-detail'),
    path('<int:recipe_pk>/non-wh-ingredient/<int:ingredient_pk>/update/', login_required(views.NonWarehouseIngredientUpdateView.as_view()), name='non-wh-ingredient-update'),
    path('<int:recipe_pk>/non-wh-ingredient/<int:ingredient_pk>/delete/', login_required(views.NonWarehouseIngredientDeleteView.as_view()), name='non-wh-ingredient-delete'),
    path('<int:recipe_pk>/non-wh-ingredient/', login_required(views.NonWarehouseIngredientListView.as_view()), name='non-wh-ingredient-list'),

    # NonWarehouseProduct CRUD
    path('non-wh-product/', login_required(views.NonWarehouseProductListView.as_view()), name='non-wh-product-list'),
    path('non-wh-product/create/', login_required(views.NonWarehouseProductCreateView.as_view()), name='non-wh-product-create'),
    path('non-wh-product/<int:pk>/', login_required(views.NonWarehouseProductDetailView.as_view()), name='non-wh-product-detail'),
    path('non-wh-product/<int:pk>/update/', login_required(views.NonWarehouseProductUpdateView.as_view()), name='non-wh-product-update'),
    path('non-wh-product/<int:pk>/delete/', login_required(views.NonWarehouseProductDeleteView.as_view()), name='non-wh-product-delete'),
]