from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
import requests
import hmac
import hashlib


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print("lola")
        if form.is_valid():
            form.save()
            print("sala")
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
        products = Product.objects.get(id=product_id)
        quantity = request.POST.get('quantity')
        if int(quantity) <= int(products.qty):

            total = int(products.price) * int(quantity)
            response = requests.post('https://api.razorpay.com/v1/orders',
            json={
            'amount': total*100,
            'currency': 'INR',
            'payment_capture':1
            },
            headers={'content-type':'application/json',
            'Authorization': 'Basic cnpwX3Rlc3RfWk13MklkM3JsZExrbTA6UjdQaFRYaVdqb0o1WW9lc0FJNGRpUlJR'
            }).json()
            amount = response.get('amount')
            order_id = response.get('id')
            return render(request, 'razorpay_form.html', {
                'amount': amount,
                'order_id': order_id,
                'name': products.name,
                'product_id': products.id,
                'total': total,
                'quantity': quantity
            })
        else:
            return render(request, 'order.html', {'error':"Quantity is Not Available"})

def feedback(request):
    if request.method == 'GET':
        return render(request, 'feedback.html')
    else:
        email = request.POST.get('email')
        message = request.POST.get('msg')
        send_mail('disinfecto', message, email, ['rishabh.verma11998@gmail.com'])
        print("suexsuces")
        return redirect('home')


def success(request):
    if request.method == 'POST':
        if 'error' in request.POST:
            return HttpResponse('payment not completed')
        else:
            # got the response postback data
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_signature = request.POST.get('razorpay_signature')
            # payment string
            payment_string = razorpay_order_id + '|' + razorpay_payment_id
            # generate the hashed string
            signature = hmac.new(bytes('R7PhTXiWjoJ5YoesAI4diRRQ', 'latin-1'),
            msg=bytes(payment_string, 'latin-1'),
            digestmod=hashlib.sha256
            ).hexdigest().upper()
            # verify the payment integrity
            if signature == razorpay_signature:
                product = Product.objects.get(id=int(request.POST.get('product')))
                Order.objects.create(
                    user=request.user,
                    product=product,
                    quantity=request.POST.get('quantity'),
                    total=request.POST.get('total'),
                    razorpay_order_id=razorpay_order_id,
                    order_success=True
                )
                product.qty = int(product.qty) - int(request.POST.get('quantity'))
                return HttpResponse('Payment done Order placed successfully')
            else:
                return HttpResponse('payment failed')

def index(request):
    if request.method == 'GET':
        return render(request, 'home.html')
