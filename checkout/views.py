from django.shortcuts import render , redirect
from checkout.forms import UserInfoForm
from store.models import Cart , Product , Order


def Make_order(request):
    if request.method != 'POST':
        return redirect('store.checkout')
    
    form = UserInfoForm(request.POST)
    if form.is_valid():
         #To Create the order, we need user data and the products, we can get it from the form and the cart
        cart = Cart.objects.filter(session=request.session.session_key).last() #The last cart of the user
        products = Product.objects.filter(pk__in=cart.items)

        total = 0
        for item in products:
            total+=item.price
        
        if total <= 0:
            return redirect('store.checkout')
        
        order = Order.objects.create(customer=form.cleaned_data  , total = total) #form.cleaned_data = the object

        for product in products:
            order.orderproduct_set.create(
                Product_id = product.id,
                price = product.price
            )
        
        Cart.objects.filter(session=request.session.session_key).delete()

        return redirect('store.checkout_complete')
    else:
        return redirect('store.checkout')        

