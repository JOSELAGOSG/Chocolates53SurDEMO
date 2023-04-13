from django import forms
from .models import Purchase, Box, Freight, Payment
from datetime import date

SHELF_CHOICES = [('E1', 'Estante 1'), ('E2', 'Estante 2'), ('E3', 'Estante 3'), ('E4', 'Estante 4'), ('LP', 'Lateral Puerta')]
PURCHASE_YEARS = ['2021', '2022', '2023']
BOX_EXPIRATION_YEARS = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030']
MONTHS = {
    1:('Enero'), 2:('Febrero'), 3:('Marzo'), 4:('Abril'),
    5:('Mayo'), 6:('Junio'), 7:('Julio'), 8:('Agosto'),
    9:('Septiembre'), 10:('Octubre'), 11:('Noviembre'), 12:('Diciembre')
}

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['invoice_number', 'date', 'provider', 'seller_name']
        widgets = {
            'date' : forms.SelectDateWidget(years=PURCHASE_YEARS, months=MONTHS)
        }

class FreightForm(forms.ModelForm):
    class Meta:
        model = Freight
        fields = ['invoice_number', 'company', 'application_date', 'price_without_taxes']
        widgets = {
        'application_date' : forms.SelectDateWidget(years=PURCHASE_YEARS, months=MONTHS)
        }

class BoxExpirationForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = ['expiration_date']
        widgets = {
            'expiration_date' : forms.SelectDateWidget(years=BOX_EXPIRATION_YEARS, months=MONTHS)
        }

class BoxShelfForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = ['shelf']
        widgets = {
            'shelf' : forms.Select(choices=SHELF_CHOICES)
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'date' : forms.SelectDateWidget(years=PURCHASE_YEARS, months=MONTHS),
            
        }
class BoxWithdrawalForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = ['in_warehouse', 'withdrawal_date']
        widgets = {
            'in_warehouse': forms.HiddenInput(),
            'whithdrawal_date': forms.HiddenInput(),
        }