from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from .forms import *
from .models import *
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from ast import literal_eval
from django.db.models import Sum
import requests
import hmac
import hashlib


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('product:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {
        'form': form
    })


@login_required
def home(request):
    if request.method == 'GET':
        products = Product.objects.all()
        return render(request, 'products.html', {
            'products':products
        })


@login_required
def getServices(request):
    if request.method == 'GET':
        services = Service.objects.all()
        return render(request, 'services.html', {
            'services': services
        })


@login_required
def payment(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        # razorpay data payload
        data = literal_eval(data)
        # razorpay_payment_url
        razorpay_payment_url = 'https://api.razorpay.com/v1/orders'
        # razorpay headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic cnpwX3Rlc3RfWk13MklkM3JsZExrbTA6UjdQaFRYaVdqb0o1WW9lc0FJNGRpUlJR'
        }
        response = requests.post(razorpay_payment_url,
            json=data,
            headers=headers
        ).json()

        return JsonResponse({
            'amount': response.get('amount'),
            'order_id': response.get('id')           
        })
    else:
        return render(request, 'razorpay_form.html', {
            'amount': request.GET.get('amount'),
            'order_id': request.GET.get('id')
        })


# @login_required
# def productorder(request, product_id):
#     if request.method == 'GET':
#         products = Product.objects.get(id=int(product_id))
#         return render(request, 'order.html', {'products':products})
#     else:
#         products = Product.objects.get(id=product_id)
#         quantity = request.POST.get('quantity')
#         if int(quantity) <= int(products.qty):

#             total = int(products.price) * int(quantity)
#             response = requests.post('https://api.razorpay.com/v1/orders',
#             json={
#             'amount': total*100,
#             'currency': 'INR',
#             'payment_capture':1
#             },
#             headers={'content-type':'application/json',
#             'Authorization': 'Basic cnpwX3Rlc3RfWk13MklkM3JsZExrbTA6UjdQaFRYaVdqb0o1WW9lc0FJNGRpUlJR'
#             }).json()
#             amount = response.get('amount')
#             order_id = response.get('id')
#             return render(request, 'razorpay_form.html', {
#                 'amount': amount,
#                 'order_id': order_id,
#                 'name': products.name,
#                 'product_id': products.id,
#                 'total': total,
#                 'quantity': quantity
#             })
#         else:
#             return render(request, 'order.html', {'error':"Quantity is Not Available"})


@login_required
def feedback(request):
    if request.method == 'GET':
        return render(request, 'feedback.html')
    else:
        email = request.POST.get('email')
        message = request.POST.get('msg')
        send_mail('Dr Disinfecto Customer FeedBack', message, email, [settings.EMAIL_HOST_USER])
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
                items = Cart.objects.filter(user=request.user.pk)
                for item in items:
                    product = Product.objects.get(id=item.product.pk)
                    product.qty = int(product.qty) - int(item.quantity)
                    product.save()
                items.delete()
                return HttpResponse('Payment done Order placed successfully')
            else:
                return HttpResponse('payment failed')


def index(request):
    if request.method == 'GET':
        images = BannerImage.objects.all()
        reviews = Review.objects.all()
        return render(request, 'home.html', {
            'images': images,
            'reviews': reviews
        })


def getAllProducts(request):
    if request.method == 'GET':
        products = Product.objects.all()
        return render(request, 'index.html', {
            'products': products
        })


@login_required
def giveReview(request):
    if request.method == 'GET':
        return render(request, 'review.html', {
            'username': request.user.first_name
        })
    else:
        Review.objects.create(
            user=request.user,
            product_name=request.POST.get('product_name'),
            review_text=request.POST.get('review'),
            ratings=request.POST.get('rating')
        )
        return redirect('product:home')


def inquiry(request):
    if request.method == 'POST':
        message = f'''
            This is the formal inquiry by the customer {request.POST.get('customer_name')} \n
            Customer additonal details:- \n
            Email- {request.POST.get('email')}\n
            Phone Number- {request.POST.get('phone')}\n
            Inquiry is below :-\n
            {request.POST.get('inquiry_text')}
        '''
        send_mail('Dr Disinfecto Customer Inquiry', message, request.POST.get('email'), [settings.EMAIL_HOST_USER])
        return redirect('product:index')


def complaint(request):
    if request.method == 'POST':
        message = f'''
            This is the complaint by the customer {request.POST.get('customer_name')} \n
            Customer additonal details:- \n
            Email- {request.POST.get('email')}\n
            Phone Number- {request.POST.get('phone')}\n
            Complaint is below :-\n
            {request.POST.get('complaint_text')} 
        '''
        send_mail('Dr Disinfecto Customer Complaint', message, request.POST.get('email'), [settings.EMAIL_HOST_USER])
        return redirect('product:index')


@login_required
def addtocart(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data = literal_eval(data)
        print(data)
        if data.get('product'):
            product = Product.objects.get(id=data.get('id'))
            total_price = product.price * data.get('quantity')
            Cart.objects.create(
                user=request.user,
                product=product,
                quantity=data.get('quantity'),
                price=total_price
            )
            return HttpResponse("product added into cart")
        else:
            print("sada")
            service = Service.objects.get(id=data.get('id'))
            Cart.objects.create(
                user=request.user,
                service=service,
                quantity=0,
                price=service.price
            )
            return HttpResponse("service added into cart")
    elif request.method == 'DELETE':
        Cart.objects.get(pk=request.GET.get('id'), user=request.user.pk).delete()
        return HttpResponse("product removed from cart")


@login_required
def showcart(request):
    if request.method == 'GET':
        items = Cart.objects.filter(user=request.user.pk)
        total_price = Cart.objects.filter(user=request.user.pk).aggregate(Sum('price'))['price__sum']
        return render(request, 'cartitems.html', {
            'items': items,
            'total_price': total_price
        })