from .cart import Cart

# Create context processor so cart can be accessible across the app

def cart(request):
    # Return the default data from the Cart
    return {'cart': Cart(request)}