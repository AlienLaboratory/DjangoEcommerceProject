from shop.models import Product, Profile

def update_cart_state(self):
         # Logic for logged in user
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Convert object format {'1':2} to {"1":2}
            scart = str(self.cart)
            scart = scart.replace("\'","\"")
            #Save cart for persistance to profile
            current_user.update(old_cart=scart)

class Cart():
    def __init__(self, request):
        self.session = request.session

        #Get request
        self.request = request

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new then no session key available = create the one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages of site
        # Context processors?
        self.cart = cart

    
    

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        update_cart_state(self)

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        update_cart_state(self)


    def __len__(self):
        return len(self.cart)
    
    def get_products(self):
        #Get ids from cart
        product_ids = self.cart.keys()
        # Look up products in database with ids
        products = Product.objects.filter(id__in=product_ids)

        return products
    
    def get_quantities(self):
       
        quantities = self.cart
        return quantities
    

    def update_quantity(self, product, quantity):
        #Get ids from cart
        product_id = str(product)
        # Look up products in database with ids
        product_qty = int(quantity)
        #get cart
        cart = self.cart
        # update cart dictionary 
        cart[product_id] = product_qty

        self.session.modified = True

        update_cart_state(self)

        return self.cart
    
    def delete_product(self, product):
        #Get ids from cart
        product_id = str(product)

        #get cart
        cart = self.cart
        # delete from cart dictionary 
        if product_id in cart:
            del cart[product_id]

        self.session.modified = True

        update_cart_state(self)

        return self.cart
    

    def cart_total(self):
         #Get ids from cart
        product_ids = self.cart.keys()
        # Look up products in database with ids
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart
        total = 0
        for key, value in cart.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)

        return total
