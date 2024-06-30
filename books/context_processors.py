from .cart import Cart
from django.conf import settings


def cart(request):
    return {"cart": Cart(request)}


def getCartContent(request):

    return {'cart_content': Cart(request)}
