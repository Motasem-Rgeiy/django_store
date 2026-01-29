from django.shortcuts import render
from store.models import Product , Slider , Category , Cart
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from django.http import JsonResponse

def index(request):
    models = Product.objects.select_related('author').filter(featured=True)
    slides = Slider.objects.order_by('order')
    return  render(request , 'index.html' , {'products':models , 'slides':slides})

def product(request , pid):
    model = Product.objects.get(pk=pid)
    return render(request , 'product.html' ,{'product':model})


def category(request , cid=None):
    cat = None
    cid = request.GET.get('cid') #Get the current id of the category
    query = request.GET.get('query')
    where = {}
    if cid:
        cat = Category.objects.get(pk=cid)
        where['Category_id'] = cid #Get the id of a specific category

    if query:
        where['name__icontains'] = query

    models = Product.objects.filter(**where) #Get all products of a specific category
    paginator = Paginator(models , 9) #Per page
    page_number = request.GET.get('page') #Return current page
    page_obj = paginator.get_page(page_number) #page object used for operations
    return render(request,'category.html' , {'cat':cat , 'page_obj':page_obj})



def cart(request):
    return render(request , 'cart.html')

def checkout(request):
    return render(request , 'checkout.html')

def checkout_complete(request):
    return render(request , 'checkout-complete.html')


def cart_add(request , pid):
    if not request.session.session_key: 
        request.session.create() #If there is no session key from the request, means there is no session, so we create a session

    session_id = request.session.session_key #Return the session id after create(if it is not created yet)
    cart_model = Cart.objects.filter(session=request.session.session_key).last() #Return the the required products of the specific cart based on the session key

    if cart_model is None: 
        cart_model = Cart.objects.create(session_id=session_id , items=[pid]) #if the cart has no products, we create a new cart
    
    elif pid not in cart_model.items:  
        cart_model.items.append(pid) #if we have products in the cart, we add it directly
        cart_model.save()
    
    return JsonResponse({
            'message':_('The product has been added to your cart'),  #To display a message that a the product has been added to the cart successfully
            'items_count':len(cart_model.items)
         })

def cart_remove(request , pid):
    session = request.session.session_key

    if not session:
        return JsonResponse({})
    
    cart_model = Cart.objects.filter(session=request.session.session_key).last()

    if not cart_model:
        return JsonResponse({})
    
    cart_model.items.remove(pid)
    cart_model.save()

    return JsonResponse({
            'message':_('The product has been removed from your cart'), 
            'items_count':len(cart_model.items)
         })
