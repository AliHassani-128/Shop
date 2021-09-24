from django.shortcuts import render, redirect


# Create your views here.


def index(request):
    # return render(request, 'core/base.html')
    return redirect('product:show_products')

