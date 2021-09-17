from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.views import generic

from customer.forms import CustomerForm, AddressForm, EditAddressForm
from customer.models import Customer, Address


def update_profile(request,pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        messages.error(request, 'Just Customers can edit their profile')
        return redirect('core:index')

    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile edited successfully')
            return redirect('core:index')

    elif request.method == 'GET':

        form = CustomerForm(instance=customer)
        return render(request,'customer/update_profile.html',{'form':form})


@login_required
def set_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.customer = Customer.objects.get(id=request.user.id)
            instance.country = request.POST.get('country')
            instance.city = request.POST.get('city')
            instance.save()
            messages.success(request, f'Address for user {request.user.username} saved')
            return redirect('customer:show_address')
        else:
            print('Not valid')

    elif request.method == 'GET':
        return render(request,'customer/address_form.html')


class ShowCustomerAddress(generic.ListView):
    model = Address
    template_name = 'customer/show_customer_address.html'
    def get_queryset(self):
        self.addresses = Address.objects.filter(customer_id=self.request.user.id)
        return self.addresses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = self.addresses
        return context


@login_required
def edit_address(request,pk):
    address = Address.objects.get(id=pk)
    if request.method == "POST":
        form = EditAddressForm(request.POST,instance=address)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.customer = Customer.objects.get(id=request.user.id)
            instance.save()
            return redirect('customer:show_address')
    elif request.method == 'GET':
        form = EditAddressForm(instance=address)
        return render(request,'customer/address_form.html',{'form':form,'id':address.id})



@login_required
def delete_address(request,pk):
    Address.objects.get(id=pk).delete()
    messages.success(request, 'Selected address deleted')
    return redirect('customer:show_address')




