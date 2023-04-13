#PRODUCTOS MEDIDOS EN UNIDADES
from django import template

register = template.Library()

@register.filter
def products_unities(products):
    amounts_list = []
    for product in products:
        if product.measurement == 'un':
            amounts_list.append(product.get_total_amount_in_warehouse())
    return amounts_list