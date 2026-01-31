from django.shortcuts import render , redirect
from checkout.forms import UserInfoForm
from store.models import Cart , Product , Order
from checkout.models import Transaction ,PaymentMethod
from django.template.loader import render_to_string
from django.core.mail import send_mail
import math
'''
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
        
        order = Order.objects.create(customer=form.cleaned_data  , total = total) #form.cleaned_data = the object(dict)

        for product in products:
            order.orderproduct_set.create(
                Product_id = product.id,
                price = product.price
            )
        send_order_email(order , products)
        
        Cart.objects.filter(session=request.session.session_key).delete()

        return redirect('store.checkout_complete')
    else:
        return redirect('store.checkout')        
'''

def stripe_transaction(request):
    transaction = Make_transaction(request ,PaymentMethod.Stripe )

def paypal_transaction(request):
    transaction = Make_transaction(request ,PaymentMethod.Paypal )


def Make_transaction(request , pm):
    
    form = UserInfoForm(request.POST)
    if form.is_valid():
         #To Create the order, we need user data and the products, we can get it from the form and the cart
        cart = Cart.objects.filter(session=request.session.session_key).last() #The last cart of the user
        products = Product.objects.filter(pk__in=cart.items)

        total = 0
        for item in products:
            total+=item.price
        
        if total <= 0:
            return None
        
        return Transaction.objects.create(
            customer = form.cleaned_data,
            session = request.session.session_key,
            payment_method = pm,
            items = cart.items,
            amount = math.ceil(total),
        ) 

    else:
        return redirect('store.checkout')      



def send_order_email(order , products):
    msg_html = render_to_string('emails/order.html' , 
            {
                'order':order,
                'products':products
            }
            )

    send_mail(
        subject='Order Completed',
        html_message=msg_html,
        message=msg_html,
        from_email='motasem.example.com',
        recipient_list=[order.customer['email']],
    )

