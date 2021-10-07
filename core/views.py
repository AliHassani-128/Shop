from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from customer.models import Customer
from order.models import Order
from product.models import Product, Category
from django.utils.translation import gettext_lazy as _

def index(request):
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

    return render(request, 'product/all_products_drf.html', {'categories': categories, 'last_products': last_products})


def search(request):
    if request.method == 'POST':
        item = request.POST.get('search')
        products = Product.objects.filter(Q(name__icontains=item) | Q(category__name__icontains=item))
        if len(products) == 0:
            messages.error(request, _('Product with this name Not Found!!'))
            return redirect('core:index')
        return render(request, 'product/all_products.html', {'products': products},status=200)
