# PRODUCTOS MEDIDOS EN KILOS
from django import template

register = template.Library()

@register.filter
def products_amounts(products):
    amounts_list = []
    for product in products:
        if product.measurement == 'kg':
            amounts_list.append(product.get_total_amount_in_warehouse())
    return amounts_list