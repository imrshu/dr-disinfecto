from django.template import Library
from product.models import Product, Service

register = Library()


@register.filter(name='times')
def times(value):
    return range(value)


@register.filter(name='getname')
def getProductName(value):
    return Product.objects.get(id=int(value)).name


@register.filter(name='getsname')
def getServiceName(value):
    return Service.objects.get(id=int(value)).name

