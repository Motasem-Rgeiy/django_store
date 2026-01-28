from django import template
register = template.Library()

def currency(price):
    return '{:.2f}'.format(price) + ' $'

register.filter('currency' , currency)