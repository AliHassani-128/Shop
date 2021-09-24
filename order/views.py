import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render, redirect

from customer.models import Customer
from order.models import Order, OrderHistory
from product.models import Product


def order_total_price(orders):
    total_price = 0
    for order in orders:
        total_price += order.product_price
    return total_price


def delete_from_cart(request):
    product_id = request.GET.get('product')
    customer = Customer.objects.get(id=request.user.id)
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart')

    if product_id in cart.keys():
        if product.inventory >= 1:
            order = Order.objects.get(product=product, customer=customer, ordered=False)
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
    customer = Customer.objects.get(id=request.user.id)
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
    customer = Customer.objects.get(id=request.user.id)
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart')

    if cart:
        if product_id in cart.keys():
            if product.inventory >= 1:
                order = Order.objects.get(product=product, customer=customer, ordered=False)
                order.quantity += 1
                product.inventory -= 1
                order.save()
                product.save()
                cart[product_id] = order.quantity

                return HttpResponse(
                    json.dumps({'products': len(Order.objects.filter(customer=customer, ordered=False))}),
                    content_type="application/json")
            else:
                return HttpResponse(status=400)
        else:
            cart[product_id] = 1
            Order.objects.create(product=product, quantity=1, customer=customer)
            request.session['cart'] = cart
            return HttpResponse(json.dumps({'products': len(Order.objects.filter(customer=customer, ordered=False))}),
                                content_type="application/json")
    else:

        cart = dict()
        cart[product_id] = 1
        Order.objects.create(product=product, quantity=1, customer=customer)
        request.session['cart'] = cart
        return HttpResponse(json.dumps({'products': len(Order.objects.filter(customer=customer, ordered=False))}),
                            content_type="application/json")


def order_list(request):
    orders = Order.objects.filter(customer_id=request.user.id, ordered=False)
    total_price = order_total_price(orders)
    return render(request, 'order/all_orders.html', {'orders': orders, 'total_price': total_price})


@login_required
def final_order(request):
    customer = Customer.objects.get(id=request.user.id)
    if not customer.order_history.filter(ordered=False).exists() :
        if Order.objects.filter(customer=customer,ordered=False).exists():
            orders = Order.objects.filter(customer=customer, ordered=False)
            order_history = OrderHistory.objects.create(customer=customer)
            order_history.orders.add(*orders)
            order_history.save()
            for order in orders:
                order.ordered = True
                order.save()
            request.session['cart'] = {}
        else:
            return redirect('core:index')
    else:
        order_history = OrderHistory.objects.get(customer=customer,ordered=False)
    return render(request, 'order/final_order.html', {'order_history': order_history})

@login_required
def final_pay(request,id):
    order_history = OrderHistory.objects.get(id=id)
    order_history.ordered = True
    order_history.save()
    messages.info(request, 'You will redirect to paying page')
    return redirect('core:index')
