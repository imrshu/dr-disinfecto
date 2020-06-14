from django.template import Library
from product.models import Product

register = Library()


@register.filter(name='times')
def times(value):
    return range(value)


@register.filter(name='getname')
def getProductName(value):
    return Product.objects.get(id=int(value)).name