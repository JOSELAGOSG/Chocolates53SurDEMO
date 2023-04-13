#PRODUCTOS MEDIDOS EN UNIDADES
from django import template

register = template.Library()

@register.filter
def products_unities_names(products):
    names_list = []
    for product in products:
        if product.measurement == 'un':
            names_list.append(product.name)
    return names_list