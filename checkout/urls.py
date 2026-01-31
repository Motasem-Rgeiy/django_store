from django.urls import path
from . import views
urlpatterns = [
  #  path('order' , views.Make_order , name='checkout.order'),
  path('stripe' , views.stripe_transaction , name= 'checkout.stripe'),
  path('paypal' , views.paypal_transaction , name= 'checkout.paypal')

]