from django.db import models
from django.urls import reverse
from datetime import date, timedelta


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('warehouse:brand-detail', args=[self.pk])
    
    def get_update_url(self):
        return reverse('warehouse:brand-update', args=[self.pk])

    def get_delete_url(self):
        return reverse('warehouse:brand-delete', args=[self.pk])
    

class Product(models.Model):
    MEASUREMENT_CHOICES = [('kg', 'kilogramos'), ('un', 'unidades')]
    name = models.CharField(max_length=100, unique=True)
    brand = models.ForeignKey(Brand, related_name='product', on_delete=models.PROTECT)
    measurement = models.CharField(choices=MEASUREMENT_CHOICES, default='kg', max_length=2)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('warehouse:product-detail', args=[self.pk])
    
    # Get amount related info
    def get_total_amount_in_warehouse(self): #Tambien sirve para unidades (mejor cambiar nombre xd)
        amount = 0
        for box in self.boxes.all():
            if box.in_warehouse:
                amount += box.amount
        return amount
    
    def get_total_amount_withdrawn(self):
        amount = 0
        for box in self.boxes.all():
            if not box.in_warehouse:
                amount += box.amount
        return amount
    
    def get_total_amount(self):
        return self.get_total_amount_in_warehouse() + self.get_total_amount_withdrawn()

    # Get monetary value related info

    def get_total_value_in_warehouse(self):
        value = 0 
        for box in self.boxes.all():
            if box.in_warehouse:
                value += box.get_price_with_taxes()
        return(value)
    
    def get_total_value_withdrawn(self):
        value = 0 
        for box in self.boxes.all():
            if not box.in_warehouse:
                value += box.get_price_with_taxes()
        return(value)

    # Get amount of boxes in warehouse
    def get_boxes_amount_in_warehouse(self):
        amount = 0
        for box in self.boxes.all():
            if box.in_warehouse:
                amount += 1
        return amount
    
    # Get amount soon to expire

    def get_amount_soon_to_expire_in_warehouse(self):
        amount = 0
        for box in self.boxes.filter(in_warehouse=True):
            if box.soon_to_expire():
                amount += box.amount
        return amount
    

    def get_highest_price_per_un_of_measurement(self):
        highest_price_per_un_of_measurement = 0
        for box in self.boxes.filter(in_warehouse=True):
            if box.amount > 0:
                price_per_un_of_measurement = box.price / box.amount
                if price_per_un_of_measurement > highest_price_per_un_of_measurement:
                    highest_price_per_un_of_measurement = price_per_un_of_measurement
        return highest_price_per_un_of_measurement


    def get_update_url(self):
        return reverse('warehouse:product-update', args=[self.pk])

    def get_delete_url(self):
        return reverse('warehouse:product-delete', args=[self.pk])

class Provider(models.Model):
    rut = models.CharField(max_length=11, unique=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=12)
    address = models.TextField(null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('warehouse:provider-detail', args=[self.pk])
    
    def get_update_url(self):
        return reverse('warehouse:provider-update', args=[self.pk])

    def get_delete_url(self):
        return reverse('warehouse:provider-delete', args=[self.pk])


class Payment(models.Model):
    METHOD_CHOICES = [('TRF','Transferencia'), ('CRD','Tarjeta') ,('CSH','Efectivo')]
    PAID_BY_CHOICES = [('C53','Chocolates 53 Sur'), ('ALE','Alejandra'), ('LOR','Lorena')]

    date = models.DateField()
    method = models.CharField(choices=METHOD_CHOICES, max_length=3)
    paid_by = models.CharField(choices=PAID_BY_CHOICES, max_length=3)

    def get_absolute_url(self):
        return reverse('warehouse:payment-detail', args=[self.pk])


class FreightCompany(models.Model):
    rut = models.CharField(max_length=11, unique=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    address = models.TextField(null=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("warehouse:freightCompany-detail", args=[self.pk])
    
    def get_update_url(self):
        return reverse('warehouse:freightCompany-update', args=[self.pk])

    def get_delete_url(self):
        return reverse('warehouse:freightCompany-delete', args=[self.pk])
    

class Freight(models.Model):
    invoice_number = models.BigIntegerField()
    company = models.ForeignKey(FreightCompany, related_name='company', on_delete=models.CASCADE)
    reception_date = models.DateField(null=True)
    application_date = models.DateField()
    price_without_taxes = models.IntegerField()
    payment = models.ForeignKey(Payment, related_name='freight_payment', null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return 'Flete ID: ' + str(self.pk)
    
    def get_absolute_url(self):
        return reverse('warehouse:freight-detail', args=[self.pk])
    
    def get_create_payment_url(self):
        return reverse('warehouse:freight-payment-create', args=[self.pk])

class Purchase(models.Model):
    invoice_number = models.BigIntegerField(null=True)
    date = models.DateField()
    provider = models.ForeignKey(Provider, related_name='purchase', on_delete=models.CASCADE)
    seller_name = models.CharField(max_length=50, blank=True, null=True)
    freight = models.ForeignKey(Freight, related_name='purchase', null=True, on_delete=models.SET_NULL)
    payment = models.ForeignKey(Payment, related_name='purchase', null=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse('warehouse:purchase-detail', args=[self.pk])
    
    def get_create_item_url(self):
        return reverse('warehouse:item-create', args=[self.pk])
    
    def get_create_freight_url(self):
        return reverse('warehouse:freight-create', args=[self.pk])
    
    def get_create_payment_url(self):
        return reverse('warehouse:purchase-payment-create', args=[self.pk])

    def get_total_price(self):
        price = 0 
        for item in self.item.all():
            price += item.get_total_price()
        
        return price
    
    def get_total_price_plus_freight_price(self):
        purchase_price = self.get_total_price()
        freight_price_without_taxes = self.freight.price_without_taxes
        
        return purchase_price + freight_price_without_taxes
    
    def get_total_price_with_taxes(self):
        price = self.get_total_price()
        return round(price * 1.19)
    
    def get_total_amount(self):
        amount = 0
        for item in self.item.all():
            amount += item.boxes_quantity * item.amount_per_box 
        return amount

    def get_freight_price_per_un_of_measurement(self):
        total_amount = self.get_total_amount()
        if self.freight and total_amount != 0:
            return round(self.freight.price_without_taxes / total_amount)
        return 0

    def get_update_url(self):
        return reverse('warehouse:purchase-update', args=[self.pk])

    def get_delete_url(self):
        return reverse('warehouse:purchase-delete', args=[self.pk])

    class Meta:
        ordering = ['-date']


class PurchaseItem(models.Model):
    product = models.ForeignKey(Product, related_name='purchase_item', on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, related_name='item', on_delete=models.CASCADE)
    boxes_quantity = models.IntegerField()
    amount_per_box = models.IntegerField()
    price_per_box = models.IntegerField()

    def __str__(self):
        return f'Compra: {self.purchase.pk} | Item: {self.pk}'
    
    def get_total_price(self):
        return self.price_per_box * self.boxes_quantity

    def get_price_per_un_of_measurement(self):
        if self.amount_per_box != 0:
            return  round(self.price_per_box / self.amount_per_box)
    
    def get_price_per_un_of_measurement_plus_freight_price_per_kg(self):
        price_per_kg = self.get_price_per_un_of_measurement()
        freight_price_per_kg = self.purchase.get_freight_price_per_un_of_measurement()
        return price_per_kg + freight_price_per_kg

    def get_absolute_url(self):
        return reverse('warehouse:item-detail', args=[self.pk])

class Box(models.Model):
    SHELF_CHOICES = [('E1', 'Estante 1'), ('E2', 'Estante 2'), ('E3', 'Estante 3'), ('E4', 'Estante 4'), ('LP', 'Lateral Puerta')]
    product = models.ForeignKey(Product, related_name='boxes', on_delete=models.CASCADE)
    purchase_item = models.ForeignKey(PurchaseItem, related_name='boxes', on_delete=models.CASCADE)
    amount = models.IntegerField()
    price = models.IntegerField()
    expiration_date = models.DateField(null=True)
    shelf = models.CharField(choices=SHELF_CHOICES, max_length=3, null=True)
    id_warehouse = models.IntegerField(null=True)
    in_warehouse = models.BooleanField(default=True, null=True)
    withdrawal_date = models.DateField(null=True, default=None)
    

    class Meta:
        ordering = ['-in_warehouse', 'expiration_date']
        indexes = [
            models.Index(fields=['in_warehouse', 'id']),
        ]
        

    def __str__(self):
        return f'Box:{self.pk}|Product:{self.product.name}'
    
    def get_price_with_taxes(self):
        return round(self.price * 1.19)

    def withdraw(self):
        self.in_warehouse = False
        self.save()
    
    def soon_to_expire(self):
        if self.expiration_date:
            now = date.today()
            delta = timedelta(weeks=26) #WEEKS: CANTIDAD DE SEMANAS EN LAS QUE SE CONSIDERA PRONTO A EXPIRAR   
            if self.expiration_date - now <= delta:
                return True
        return False

    def get_absolute_url(self):
        return reverse('warehouse:box-detail', args=[self.pk])
    
    def get_withdraw_url(self):
        return reverse('warehouse:box-withdraw', args=[self.pk])

    def get_expiration_url(self):
        return reverse('warehouse:box-expiration', args=[self.pk])

    def get_id_url(self):
        return reverse('warehouse:box-warehouse-id', args=[self.pk])

    def get_shelf_url(self):
        return reverse('warehouse:box-shelf', args=[self.pk])
    
    