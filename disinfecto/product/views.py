from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            print(user)
            login(request, user)
            print('signup successfully')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def home(request):
    if request.method == 'GET':
        products = Product.objects.all()
        return render(request, 'index.html', {'products':products})


def productorder(request, product_id):
    if request.method == 'GET':
        products = Product.objects.get(id=int(product_id))
        return render(request, 'order.html', {'products':products})
    else:
        products = Product.objects.get(id=int(product_id))
        quantity = request.POST.get('quantity')
        total = int(products.price) * int(quantity)
        Order.objects.create(user=request.user, product=products,
        quantity=quantity, total=total)
        return redirect('home')

def feedback(request):
    if request.method == 'GET':
        return render(request, 'feedback.html')
    else:
        email = request.POST.get('email')
        message = request.POST.get('msg')
        send_mail('disinfecto', message, email, ['rishabh.verma11998@gmail.com'])
        print("suexsuces")
        return redirect('home')
