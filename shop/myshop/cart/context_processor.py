from .cart import Cart

def cart(requets):
    return {
        'cart': Cart(requets)
    }