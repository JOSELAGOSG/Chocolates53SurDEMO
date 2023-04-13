from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Brand, Product, Provider, Purchase, PurchaseItem, Box, FreightCompany, Freight, Payment
from .forms import PurchaseForm, FreightForm, BoxExpirationForm, PaymentForm, BoxShelfForm, BoxWithdrawalForm
from . import utils
from datetime import date

# Overview

def overview(request):
    
    total_amount_in_warehouse = utils.get_total_amount_in_warehouse()
    total_amount_withdrawn = utils.get_total_amount_withdrawn()

    total_value_in_warehouse = utils.get_total_value_in_warehouse()
    total_value_withdrawn = utils.get_total_value_withdrawn()

    boxes_amount_in_warehouse = utils.get_boxes_amount_in_warehouse()
    boxes_amount_withdrawn = utils.get_boxes_amount_withdrawn()


    #Get products stock amount info
    products_amount_stock_info = utils.get_amount_stock_per_product()
    
    #Get products stock value info
    products_value_stock_info = utils.get_value_stock_per_product()

    #Get products withdrawn amount info
    products_withdrawn_amount_info = utils.get_withdrawn_amount_per_product()

    #Get products stock value info
    products_withdrawn_value_info = utils.get_withdrawn_value_per_product()

    boxes_amount_in_warehouse_per_product = utils.get_boxes_amount_in_warehouse_per_product()
    
    amount_soon_to_expire_per_product = utils.get_amount_soon_to_expire_per_product()


    return render(
        request,
        'warehouse/overview.html',
        {
        'in_warehouse' : {
            'total_amount' : total_amount_in_warehouse,
            'total_value' : total_value_in_warehouse,
            'boxes_amount' : boxes_amount_in_warehouse,
            'boxes_amount_per_product' : boxes_amount_in_warehouse_per_product,
            'amount_soon_to_expire_per_product': amount_soon_to_expire_per_product,
            'amount_per_product' : {
                'names': list(products_amount_stock_info.keys()),
                'amounts': list(products_amount_stock_info.values())
            },
            'value_per_product' : {
                'names' : list(products_value_stock_info.keys()),
                'values' : list(products_value_stock_info.values())
            },
        },
        'withdrawn' : {
            'total_amount' : total_amount_withdrawn,
            'total_value' : total_value_withdrawn,
            'boxes_amount' : boxes_amount_withdrawn,
            'amount_per_product' : {
                'names': list(products_withdrawn_amount_info.keys()),
                'amounts': list(products_withdrawn_amount_info.values())
            },
            'value_per_product' : {
                'names' : list(products_withdrawn_value_info.keys()),
                'values' : list(products_withdrawn_value_info.values())
            },
        },
    }
    )

# Product CRUD Views

class ProductCreateView(CreateView):
    template_name = 'warehouse/product/product_form.html'
    model = Product
    fields = '__all__'


class ProductDetailView(DetailView):
    template_name = 'warehouse/product/product_detail.html'
    model = Product
    context_object_name = 'product'


class ProductUpdateView(UpdateView):
    template_name = 'warehouse/product/product_update_form.html'
    model = Product
    fields = '__all__'
    

class ProductListView(ListView):
    template_name = 'warehouse/product/product_list.html'
    model = Product
    context_object_name = 'products'


class ProductDeleteView(DeleteView):
    template_name = 'warehouse/product/product_confirm_delete.html'
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('warehouse:product-list')


# Brand CRUD Views

class BrandCreateView(CreateView):
    template_name = 'warehouse/brand/brand_form.html'
    model = Brand
    fields = '__all__'
    

class BrandUpdateView(UpdateView):
    template_name = 'warehouse/brand/brand_update_form.html'
    model = Brand
    fields = '__all__'


class BrandDetailView(SingleObjectMixin, ListView):
    template_name = 'warehouse/brand/brand_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Brand.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = self.object
        return context

    def get_queryset(self):
        return self.object.product.all()


class BrandListView(ListView):
    template_name = 'warehouse/brand/brand_list.html'
    model = Brand
    context_object_name = 'brands'


class BrandDeleteView(DeleteView):
    template_name = 'warehouse/brand/brand_confirm_delete.html'
    model = Brand
    context_object_name = 'brand'
    success_url = reverse_lazy('warehouse:brand-list')



# Provider CRUD Views

class ProviderCreateView(CreateView):
    template_name = 'warehouse/provider/provider_form.html'
    model = Provider
    fields = '__all__'


class ProviderUpdateView(UpdateView):
    template_name = 'warehouse/provider/provider_update_form.html'
    model = Provider
    fields = '__all__'


class ProviderDetailView(DetailView):
    template_name = 'warehouse/provider/provider_detail.html'
    model = Provider
    context_object_name = 'provider'


class ProviderListView(ListView):
    template_name = 'warehouse/provider/provider_list.html'
    model = Provider
    context_object_name = 'providers'


class ProviderDeleteView(DeleteView):
    template_name = 'warehouse/provider/provider_confirm_delete.html'
    model = Provider
    context_object_name = 'provider'
    success_url = reverse_lazy('warehouse:provider-list')

#Purchase CRUD Views

class PurchaseCreateView(CreateView):
    template_name = 'warehouse/purchase/purchase_form.html'
    model = Purchase
    form_class = PurchaseForm


class PurchaseUpdateView(UpdateView):
    template_name = 'warehouse/purchase/purchase_update_form.html'
    model = Purchase
    form_class = PurchaseForm


class PurchaseDetailView(SingleObjectMixin, ListView):
    template_name = 'warehouse/purchase/purchase_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Purchase.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchase'] = self.object
        return context

    def get_queryset(self):
        return self.object.item.all()


class PurchaseListView(ListView):
    template_name = 'warehouse/purchase/purchase_list.html'
    model = Purchase
    context_object_name = 'purchases'


class PurchaseDeleteView(DeleteView):
    template_name = 'warehouse/purchase/purchase_confirm_delete.html'
    model = Purchase 
    context_object_name = 'purchase'
    success_url = reverse_lazy('warehouse:purchase-list')

# Purchase Related Objects Create Views

class ItemCreateView(CreateView):
    template_name = 'warehouse/purchaseItem/purchaseitem_form.html'
    model = PurchaseItem
    fields = ['product', 'boxes_quantity', 'amount_per_box_kg', 'price_per_box']
    

    def form_valid(self, form):
        purchase = get_object_or_404(Purchase, pk=self.kwargs['purchase_pk'])
        self.object = PurchaseItem.objects.create(
            product = form.cleaned_data['product'],
            purchase = purchase,
            boxes_quantity = form.cleaned_data['boxes_quantity'],
            amount_per_box_kg = form.cleaned_data['amount_per_box_kg'],
            price_per_box = form.cleaned_data['price_per_box']
        )

        for i in range (0, self.object.boxes_quantity):
            Box.objects.create(
                product = self.object.product,
                purchase_item = self.object,
                amount_kg = self.object.amount_per_box_kg,
                price = self.object.price_per_box
            )


        return redirect(self.object.purchase.get_absolute_url())

class ItemDetailView(DetailView):
    template_name = 'warehouse/purchaseItem/purchaseitem_detail.html'
    model = PurchaseItem
    context_object_name = 'item'



class FreightCreateView(CreateView):
    template_name = 'warehouse/freight/freight_form.html'
    model = Freight
    form_class = FreightForm

    def form_valid(self, form):
        purchase = get_object_or_404(Purchase, pk=self.kwargs['purchase_pk'])
        self.object = Freight.objects.create(
            invoice_number = form.cleaned_data['invoice_number'],
            company = form.cleaned_data['company'],
            application_date = form.cleaned_data['application_date'],
            price_without_taxes = form.cleaned_data['price_without_taxes'],
        )
        purchase.freight = self.object
        purchase.save()

        return redirect(purchase.get_absolute_url())

   
# Box CRUD Views

class BoxListView(ListView):
    template_name = 'warehouse/box/box_list.html'
    model = Box
    context_object_name = 'boxes'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        context['soon_to_expire_in_warehouse_amount'] = utils.get_boxes_amount_soon_to_expire_in_warehouse()
        context['not_soon_to_expire_in_warehouse_amount'] = utils.get_boxes_amount_not_soon_to_expire_in_warehouse()
        context['in_warehouse_amount'] = utils.get_boxes_amount_in_warehouse()
        context['withdrawn_amount'] = utils.get_boxes_amount_withdrawn()
        return context

class BoxWithdrawView(UpdateView):
    template_name = 'warehouse/box/box_withdraw_form.html'
    model = Box
    fields = []

    def form_valid(self,form):
        self.object.in_warehouse = False
        self.object.withdrawal_date = date.today()
        self.object.save()
        return redirect(self.object.get_absolute_url())

class BoxUpdateWarehouseIdView(UpdateView):
    template_name = 'warehouse/box/box_id_form.html'
    model = Box
    fields = ['id_warehouse']

class BoxUpdateExpirationDateView(UpdateView):
    template_name = 'warehouse/box/box_expiration_form.html'
    model = Box
    form_class = BoxExpirationForm

class BoxUpdateShelfView(UpdateView):
    template_name = 'warehouse/box/box_shelf_form.html'
    model = Box
    form_class = BoxShelfForm

class BoxDetailView(DetailView):
    template_name = 'warehouse/box/box_detail.html'
    model = Box
    context_object_name = 'box'

# FreightCompany Views

class FreightCompanyCreateView(CreateView):
    template_name = 'warehouse/freightCompany/freightcompany_form.html'
    model = FreightCompany
    fields = '__all__'

class FreightCompanyUpdateView(UpdateView):
    template_name = 'warehouse/freightCompany/freightcompany_update_form.html'
    model = FreightCompany
    fields = '__all__'

class FreightCompanyDetailView(DetailView):
    template_name = 'warehouse/freightCompany/freightcompany_detail.html'
    model = FreightCompany
    context_object_name = 'company'

class FreightCompanyListView(ListView):
    template_name = 'warehouse/freightCompany/freightcompany_list.html'
    model = FreightCompany
    context_object_name = 'companies'

class FreightCompanyDeleteView(DeleteView):
    template_name = 'warehouse/freightCompany/freightcompany_confirm_delete.html'
    model = FreightCompany
    context_object_name = 'company'
    success_url = reverse_lazy('warehouse:freightCompany-list')

# Freight Views

class FreightDetailView(DetailView):
    template_name = 'warehouse/freight/freight_detail.html'
    model = Freight
    context_object_name = 'freight'




# Payment Views
class PurchasePaymentCreateView(CreateView):
    template_name = 'warehouse/payment/payment_form.html'
    model = Payment
    form_class = PaymentForm

    def form_valid(self, form):
        purchase = get_object_or_404(Purchase, pk=self.kwargs['purchase_pk'])
        self.object = Payment.objects.create(
            date = form.cleaned_data['date'],
            method = form.cleaned_data['method'],
            paid_by = form.cleaned_data['paid_by'],
            voucher_file = form.cleaned_data['voucher_file'],
        )
        purchase.payment = self.object
        purchase.save()

        return redirect(self.object.get_absolute_url())

class FreightPaymentCreateView(CreateView):
    template_name = 'warehouse/payment/payment_form.html'
    model = Payment
    form_class = PaymentForm

    def form_valid(self, form):
        freight = get_object_or_404(Freight, pk=self.kwargs['freight_pk'])
        self.object = Payment.objects.create(
            date = form.cleaned_data['date'],
            method = form.cleaned_data['method'],
            paid_by = form.cleaned_data['paid_by'],
            voucher_file = form.cleaned_data['voucher_file'],
        )
        freight.payment = self.object
        freight.save()
        purchase = freight.purchase.all()[:1]
        return redirect(self.object.get_absolute_url())

class PaymentDetailView(DetailView):
    template_name = 'warehouse/payment/payment_detail.html'
    model = Payment
    context_object_name = 'payment'