import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render, redirect
from django.views import generic

from customer.models import Customer, Address
from order.api.serializers import DiscountCodeSerializer
from order.models import Order, OrderHistory
from product.models import Product


def order_total_price(orders):
    total_price = 0
    for order in orders:
        total_price += order.product_price
    return total_price


def delete_from_cart(request):
    product_id = request.GET.get('product')
    try:
        customer = Customer.objects.get(id=request.user.id)
    except Customer.DoesNotExist:
        customer = None
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart')

    if cart:
        if product_id in cart.keys():
            if product.inventory >= 1:
                order = Order.objects.get(product=product, customer=customer, ordered=False)
                if order.quantity == 1:
                    id = order.id
                    order.delete()
                    del cart[product_id]
                    request.session['cart'] = cart
                    total_price = order_total_price(Order.objects.filter(customer_id=request.user.id, ordered=False))
                    return HttpResponse(
                        json.dumps({'delete': True, 'id': id, 'total_price': total_price}))
                else:
                    order.quantity -= 1
                    product.inventory += 1
                    order.save()
                    product.save()
                    cart[product_id] = order.quantity
                    total_price = order_total_price(Order.objects.filter(customer_id=request.user.id, ordered=False))
                    return HttpResponse(
                        json.dumps({'id': order.product.id, 'price': order.product_price, 'quantity': order.quantity,
                                    'total_price': total_price}))
            else:
                return HttpResponse(json.dumps({'error': ''}))


def add_to_cart(request):
    product_id = request.GET.get('product')
    try:
        customer = Customer.objects.get(id=request.user.id)
    except Customer.DoesNotExist:
        customer = None
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart')

    if product_id in cart.keys():
        if product.inventory >= 1:
            order = Order.objects.get(product=product, customer=customer, ordered=False)
            order.quantity += 1
            product.inventory -= 1
            order.save()
            product.save()
            cart[product_id] = order.quantity
            total_price = order_total_price(Order.objects.filter(customer_id=request.user.id, ordered=False))
            return HttpResponse(
                json.dumps({'id': order.product.id, 'price': order.product_price, 'quantity': order.quantity,
                            'total_price': total_price}))
        else:
            return HttpResponse(json.dumps({'error': 'This product does not have more inventory'}))


def add_to_cart_home_page(request):
    product_id = request.GET.get('product')
    try:
        customer = Customer.objects.get(id=request.user.id)
    except Customer.DoesNotExist:
        customer = None
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart')
    orders = request.session.get('orders')

    if cart:
        if product_id in cart.keys():
            if product.inventory >= 1:
                find_order = None
                if not customer:
                    for order_id in orders.values():
                        try:
                            find_order = Order.objects.get(id=order_id)
                            break
                        except:
                            continue

                    order = find_order
                else:
                    order = Order.objects.get(customer=customer, ordered=False, product=product)
                order.quantity += 1
                product.inventory -= 1
                order.save()
                product.save()
                cart[product_id] = order.quantity
                if customer:
                    products = len(Order.objects.filter(customer=customer, ordered=False))
                else:
                    products = len(request.session['cart'])


                return HttpResponse(
                    json.dumps({'products': products}),
                    content_type="application/json")
            else:
                return HttpResponse(status=400)
        else:
            cart[product_id] = 1
            new_order = Order.objects.create(product=product, quantity=1, customer=customer)
            request.session['cart'] = cart
            if not customer:
                orders[new_order.id] = new_order.id
                request.session['orders'] = orders
                products = len(request.session['cart'])

            else:
                products = len(Order.objects.filter(customer=customer, ordered=False))

            return HttpResponse(
                json.dumps({'products': products}),
                content_type="application/json")

    else:
        cart = dict()
        cart[product_id] = 1
        request.session['cart'] = cart
        new_order = Order.objects.create(product=product, quantity=1, customer=customer)
        if not customer:
            order = dict()
            order[new_order.id] = new_order.id
            request.session['orders'] = order
            products = len(request.session['cart'])

        else:
            products = len(Order.objects.filter(customer=customer, ordered=False))
        return HttpResponse(
            json.dumps({'products': products}),
            content_type="application/json")


def order_list(request):
    try:
        customer = Customer.objects.get(id=request.user.id)
    except Customer.DoesNotExist:
        pass
    else:
        if request.session.get('orders'):
            customer_orders_products = [order.product.id for order in Order.objects.filter(customer_id=request.user.id, ordered=False)]
            for order_id in request.session.get('orders'):
                order = Order.objects.get(id=order_id)
                if order.product.id in customer_orders_products:
                    find_order = Order.objects.get(product_id=order.product.id,customer=customer,ordered=False)
                    find_order.quantity += order.quantity
                    order.delete()
                    continue
                order.customer = customer
                order.save()
            request.session['orders'] = {}
    orders = Order.objects.filter(customer_id=request.user.id, ordered=False)
    total_price = order_total_price(orders)
    if not request.session.get('cart'):
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
    return render(request, 'order/all_orders.html', {'orders': orders, 'total_price': total_price})


@login_required
def final_order(request):
    serializer = DiscountCodeSerializer()
    customer = Customer.objects.get(id=request.user.id)
    if not customer.order_history.filter(ordered=False).exists():
        if Order.objects.filter(customer=customer, ordered=False).exists():
            orders = Order.objects.filter(customer=customer, ordered=False)
            order_history = OrderHistory.objects.create(customer=customer)
            order_history.orders.add(*orders)
            order_history.total_price = sum([order.product_price for order in orders])
            order_history.save()
            for order in orders:
                order.ordered = True
                order.save()
            request.session['cart'] = {}
            request.session['order_history'] = order_history.id

        else:
            return redirect('core:index')
    else:
        order_history = OrderHistory.objects.get(customer=customer, ordered=False)
        request.session['order_history'] = order_history.id
    if Address.objects.filter(customer_id=request.user.id).exists():
        address = Address.objects.filter(customer_id=request.user.id)
    else:
        messages.info(request, 'You should add an address in your profile first')
        return redirect('customer:set_address')

    return render(request, 'order/final_order.html',
                  {'order_history': order_history, 'address': address, 'serializer': serializer})


@login_required
def final_pay(request, id):
    try:
        order_history = OrderHistory.objects.get(id=id)
    except OrderHistory.DoesNotExist:
        messages.error(request, 'The Order History does not exists!')
        return redirect('core:index')
    address_id = request.POST.get('address')
    if not address_id:
        messages.error(request, 'You should select one address')
        return redirect('order:final_order')
    order_history.address = Address.objects.get(id=address_id)
    order_history.ordered = True
    request.session['order_history'] = {}
    order_history.save()
    messages.info(request, 'You will redirect to paying page')
    return redirect('core:index')


def delete_order(request, id):
    order = Order.objects.get(id=id)
    id = order.id
    order.delete()
    order_history = OrderHistory.objects.get(customer_id=request.user.id, ordered=False)
    order_history.orders.remove(order)
    order_history.total_price = order_total_price(order_history.orders.all())
    if order_history.orders.count() == 0:
        order_history.delete()
        request.session['order_history'] = {}
        total_price = 0
    else:
        total_price = order_history.total_price
    return HttpResponse(json.dumps({'id': id, 'total_price': total_price}))


class All_Orders_History(generic.ListView):
    model = OrderHistory
    template_name = 'order/all_orders_history.html'

    def get_queryset(self):
        return self.model.objects.filter(customer_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_history'] = self.get_queryset()
        return context
