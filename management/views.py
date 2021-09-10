from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from management.forms import ManagerForm
from management.models import Manager



def register_manager(request):
    if request.method == 'POST':
        form = ManagerForm(request.POST,request.FILES)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            image = form.cleaned_data['image']
            del form.cleaned_data['phone']
            del form.cleaned_data['image']
            user = form.save()
            manager = Manager.objects.create(phone=phone,image=image,user=user)
            login(request,user)
            return redirect('management:index')
    form = ManagerForm()
    return render(request,'customer/base.html',{'form':form})