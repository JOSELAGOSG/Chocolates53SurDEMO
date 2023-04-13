from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'warehouse'

urlpatterns = [
    path('', login_required(views.overview), name='overview'),

    path('product/', login_required(views.ProductListView.as_view()), name='product-list'),
    path('product/create/', login_required(views.ProductCreateView.as_view()), name='product-create'),
    path('product/<int:pk>/update/', login_required(views.ProductUpdateView.as_view()), name='product-update'),
    path('product/<int:pk>/delete/', login_required(views.ProductDeleteView.as_view()), name='product-delete'),
    path('product/<int:pk>/', login_required(views.ProductDetailView.as_view()), name='product-detail'),
    
    path('brand/', login_required(views.BrandListView.as_view()), name='brand-list'),
    path('brand/create/', login_required(views.BrandCreateView.as_view()), name='brand-create'),
    path('brand/<int:pk>/update/', login_required(views.BrandUpdateView.as_view()), name='brand-update'),
    path('brand/<int:pk>/delete/', login_required(views.BrandDeleteView.as_view()), name='brand-delete'),
    path('brand/<int:pk>', login_required(views.BrandDetailView.as_view()), name='brand-detail'),

    path('provider/', login_required(views.ProviderListView.as_view()), name='provider-list'),
    path('provider/create/', login_required(views.ProviderCreateView.as_view()), name='provider-create'),
    path('provider/<int:pk>/update/', login_required(views.ProviderUpdateView.as_view()), name='provider-update'),
    path('provider/<int:pk>/delete/', login_required(views.ProviderDeleteView.as_view()), name='provider-delete'),
    path('provider/<int:pk>/', login_required(views.ProviderDetailView.as_view()), name='provider-detail'),

    path('purchase/', login_required(views.PurchaseListView.as_view()), name='purchase-list'),
    path('purchase/create/', login_required(views.PurchaseCreateView.as_view()), name='purchase-create'),
    path('purchase/<int:pk>/', login_required(views.PurchaseDetailView.as_view()), name='purchase-detail'),
    path('purchase/<int:pk>/update/', login_required(views.PurchaseUpdateView.as_view()), name='purchase-update'),
    path('purchase/<int:pk>/delete/', login_required(views.PurchaseDeleteView.as_view()), name='purchase-delete'),
    path('purchase/<int:purchase_pk>/create-item/', login_required(views.ItemCreateView.as_view()), name='item-create'),
    path('purchase/<int:purchase_pk>/create-freight/', login_required(views.FreightCreateView.as_view()), name='freight-create'),
    path('purchase/<int:purchase_pk>/create-payment/', login_required(views.PurchasePaymentCreateView.as_view()), name='purchase-payment-create'),

    #path('freight/'),
    path('freight/<int:pk>', login_required(views.FreightDetailView.as_view()), name='freight-detail'),
    path('freight/<int:freight_pk>/create-payment/', login_required(views.FreightPaymentCreateView.as_view()), name='freight-payment-create'),


    #path('payment/'),
    path('payment/<int:pk>/', login_required(views.PaymentDetailView.as_view()), name='payment-detail'),


    path('item/<int:pk>/', login_required(views.ItemDetailView.as_view()), name='item-detail'),

    path('box/', login_required(views.BoxListView.as_view()), name='box-list'),
    path('box/<int:pk>/', login_required(views.BoxDetailView.as_view()), name='box-detail'),
    path('box/<int:pk>/withdraw/', login_required(views.BoxWithdrawView.as_view()), name='box-withdraw'),
    path('box/<int:pk>/update-expiration-date/', login_required(views.BoxUpdateExpirationDateView.as_view()), name='box-expiration'),
    path('box/<int:pk>/update-shelf/', login_required(views.BoxUpdateShelfView.as_view()), name='box-shelf'),    
    path('box/<int:pk>/update-warehouse-id/', login_required(views.BoxUpdateWarehouseIdView.as_view()), name='box-warehouse-id'),

    path('freightCompany/', login_required(views.FreightCompanyListView.as_view()), name='freightCompany-list'),
    path('freightCompany/create/', login_required(views.FreightCompanyCreateView.as_view()), name='freightCompany-create'),
    path('freightCompany/<int:pk>/', login_required(views.FreightCompanyDetailView.as_view()), name='freightCompany-detail'),
    path('freightCompany/<int:pk>/update/', login_required(views.FreightCompanyUpdateView.as_view()), name='freightCompany-update'),
    path('freightCompany/<int:pk>/delete/', login_required(views.FreightCompanyDeleteView.as_view()), name='freightCompany-delete'),
]
