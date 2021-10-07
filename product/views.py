from django.shortcuts import render

# Create your views here.
from django.views import generic
from customer.models import Customer
from order.models import Order
from product.models import Product, Category
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def show_products(request, id=None):
    page = request.GET.get('page', 1)
    if id:
        products_list = Product.objects.filter(category_id=id)
    else:
        products_list = Product.objects.all().order_by('-id')

    paginator = Paginator(products_list, 5)
    categories = Category.objects.all()
    last_products = Product.objects.all().order_by('-id')[:3]
    cart = request.session.get('cart')
    if not cart:
        cart = dict()
        try:
            customer = Customer.objects.get(id=request.user.id)
        except Customer.DoesNotExist:
            pass
        else:
            if Order.objects.filter(customer=customer, ordered=False).exists():
                for order in Order.objects.filter(customer=customer, ordered=False):
                    cart[str(order.product.id)] = order.quantity
                request.session['cart'] = cart

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'product/all_products.html',
                  {'products': products, 'categories': categories, 'last_products': last_products})


class ProductDetail(generic.DetailView):
    model = Product
    queryset = Product.objects.all()
    template_name = 'product/detail_product.html'
    context_object_name = 'product'
