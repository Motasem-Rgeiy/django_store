from django.urls import path
from . import views
from checkout import webhooks
from paypal.standard.ipn.views import ipn
urlpatterns = [
  #  path('order' , views.Make_order , name='checkout.order'),
  path('stripe' , views.stripe_transaction , name= 'checkout.stripe'),#Send a request when a user click checkout for stripe
  path('paypal' , views.paypal_transaction , name= 'checkout.paypal'),
  path('stripe/config'  , views.stripe_config , name='checkout.stripe.config'),
  path('stripe/webhook' ,webhooks.stripe_webhook), #receive a POST request from stripe
  path('paypal/webhook' , ipn , name='checkout.paypal-webhook')


]

