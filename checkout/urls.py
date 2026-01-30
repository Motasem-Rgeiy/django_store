from django.urls import path
from . import views
urlpatterns = [
    path('order' , views.Make_order , name='checkout.order'),
    

]