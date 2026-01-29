from django.shortcuts import render
from store.models import Product , Slider , Category
from django.core.paginator import Paginator
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