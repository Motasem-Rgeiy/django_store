from store.models import Category , Cart , Product
def store_website(request):
    categories = Category.objects.order_by('order')
    cart = Cart.objects.filter(session=request.session.session_key).last() #get the current session of the cart
    cart_total = 0
    cart_products = []
    if cart:
        cart_products = Product.objects.filter(pk__in=cart.items) #if the cart exist, get all products of this cart and calculate the total price of the products
        for item in cart_products:
            cart_total+=item.price

    return {
        'categories':categories,
        'cart_products':cart_products,
        'cart_total':cart_total
    }