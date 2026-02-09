from django.shortcuts import render , redirect
from checkout.forms import UserInfoForm , MyPayPalPaymentForm
from store.models import Cart , Product , Order
from checkout.models import Transaction ,PaymentMethod
from django.template.loader import render_to_string
from django.core.mail import send_mail
import math
from django.http import JsonResponse ,HttpResponse
from django.conf import settings
import stripe
from django.utils.translation import gettext as _

from django.urls import reverse


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



def stripe_config(request):
    return JsonResponse({
        'public_key': settings.STRIPE_PUBLISHABLE_KEY,
    })




def stripe_transaction(request):
    transaction = Make_transaction(request ,PaymentMethod.Stripe )
    if not transaction:
        return JsonResponse({
            'message':_("Please enter valid information.")
        } , status=400) #If we don't have transaction, return status 400
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount = transaction.amount * 100,
        currency=settings.CURRENCY,
        payment_method_types = ['card'],
        metadata ={
                'transaction':transaction.id
        }
    )
    #sends the secret back to the javaScript to let the stripe payment appears
    return JsonResponse({
        'client_secret': intent['client_secret'], #critical
    })






def paypal_transaction(request):
    transaction = Make_transaction(request ,PaymentMethod.Paypal )
    if not transaction:
        return JsonResponse({
            'message':_("Please enter valid information.")
        } , status=400)
    form = MyPayPalPaymentForm(initial={
        'business': settings.PAYPAL_EMAIL,
        'amount': transaction.amount,
        'invoice':transaction.id,
        'currency_code': settings.CURRENCY,
        'return_url': f'http//{request.get_host()}{reverse('store.checkout_complete')}',
        'cancel_url': f'http//{request.get_host()}{reverse('store.checkout')}',
        'notify_url':f'http://{request.get_host()}{reverse('checkout.paypal-webhook')}',
    })

    return HttpResponse(form.as_html())








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
    #cleaned_data represents the dictionary of the form {first_name:'Motasem' and so on..}
            customer = form.cleaned_data, 
            session = request.session.session_key,
            payment_method = pm,
            items = cart.items,
            amount = math.ceil(total),
        )  #status = pending (default value)

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

