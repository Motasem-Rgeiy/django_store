from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
from django.http import HttpResponse
from checkout import models
from store.models import Order , Product
from django.template.loader import render_to_string
from django.core.mail import send_mail
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

@csrf_exempt #stripe avoid this security,so we have to do it by our own
def stripe_webhook(request):
    print('stripe webhook')

    payload = request.body #The raw data Stripe sent (the "Letter")

   
    sig_header = request.META['HTTP_STRIPE_SIGNATURE'] #We get a a signature (key) to ensure that this request came from the correct place
    try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
            )
           # If the signature matches my secret, it creates an event.
    except ValueError as e:
         print("Invalid payload")
         return HttpResponse(status=400)
    
    except stripe.error.SignatureVerificationError as e:
          print('Invalid signature')
          return HttpResponse(status=400)
           

    # Handle the event
    if event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        print('payment_intent.successed')
        print(payment_intent.metadata) #It returns transaction id, so we can generate an order based on it
        transaction_id = payment_intent.metadata['transaction']
        make_order(transaction_id)
    else:
        # Unexpected event type
        print('Unhandled event type {}'.format(event['type']))
    
    return HttpResponse(status=200)

#What the difference betweeen port 200, 400, 500


@csrf_exempt
def paypal_webhook(sender , **kwargs):
     if sender.payment_status == ST_PP_COMPLETED:
          if sender.receiver_email != settings.PAYPAL_EMAIL:
               return
          print("PaymentIntent was sucessful")
          make_order(sender.invoice)

valid_ipn_received.connect(paypal_webhook)

def make_order(transaction_id):
     transaction = models.Transaction.objects.get(pk=transaction_id)
     order = Order.objects.create(transaction=transaction)
     products = Product.objects.filter(pk__in=transaction.items)
     transaction.status = models.TransactionStatus.Completed
     transaction.save()

     for product in products:
          order.orderproduct_set.create(Product_id = product.id , price=product.price)


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
        from_email='motasem@example.com',
        recipient_list=[transaction.customer_email],
    )

