#PRODUCTOS MEDIDOS EN KILOS
from django import template

register = template.Library()

@register.filter
def products_names(products):
    names_list = []
    for product in products:
        if product.measurement == 'kg':
            names_list.append(product.name)
    return names_list
