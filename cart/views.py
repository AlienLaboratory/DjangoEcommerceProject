from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from shop.models import Product
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quantities
    total = cart.cart_total()
    return render(request, "cart_summary.html", {'cart_products':cart_products,'quantities':quantities,'total':total})

def cart_add(request):
    #get cart
    cart = Cart(request)
    #check for post request
    if request.POST.get('action')=='post':
        #get products
        product_id = int(request.POST.get('product_id'))
        #get product quantity
        product_qty = int(request.POST.get('product_qty'))
        #find product in Database by id
        product = get_object_or_404(Product, id=product_id)
        #Save to the user session
        cart.add(product=product, quantity=product_qty)
        cart_count = cart.__len__()
        #Return a json response
        response = JsonResponse({'Product Name: ': product.name,'cart_count': cart_count,})
        #response = JsonResponse({'qty':product_qty})
        messages.success(request, ("Item is Successfully added to a cart"))
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action')=='post':
        #get product id
        product_id = int(request.POST.get('product_id'))
        #call delete function
        cart.delete_product(product=product_id)
        response = JsonResponse({'product':product_id})
        messages.success(request, ("Item is Successfully deleted"))
        return response
    #return redirect('cart_summary')

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action')=='post':
        #get product id
        product_id = int(request.POST.get('product_id'))
        #get product quantity
        product_qty = int(request.POST.get('product_qty'))

        cart.update_quantity(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty':product_qty})
        messages.success(request, ("Item is Successfully updated"))
        return response
        #return redirect('cart_summary')