from django.shortcuts import render
from store.models import Product , Slider , Category
from django.core.paginator import Paginator
def index(request):
    models = Product.objects.select_related('author').filter(featured=True)
    slides = Slider.objects.order_by('order')
    return  render(request , 'index.html' , {'products':models , 'slides':slides})

def product(request , pid):
    return render(request , 'product.html')


def category(request , cid=None):
    cat = None
    where = {}
    if cid:
        cat = Category.objects.get(pk=cid)
        where['Category_id'] = cid

    models = Product.objects.filter(**where)
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