from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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


@login_required
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
        star_rating = []
        images = BannerImage.objects.all()
        reviews = Review.objects.all()
        for review in reviews:
            if review.ratings:
                for i in range(int(review.ratings)):
                    star_rating.append(i)
        print(star_rating)
        return render(request, 'home.html', {
            'images': images,
            'reviews': reviews,
            'ratings': star_rating
        })

def getAllProducts(request):
    if request.method == 'GET':
        products = Product.objects.all()
        return render(request, 'products.html', {
            'products': products
        })


@login_required
def giveReview(request):
    if request.method == 'GET':
        print(request.user.first_name)
        print(request.user.email)
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
        return redirect('product:index')


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
        send_mail('Dr Disinfecto Customer Inquiry', message, request.POST.get('email'), ['rishabh.verma11998@gmail.com'])
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
        send_mail('Dr Disinfecto Customer Complaint', message, request.POST.get('email'), ['rishabh.verma11998@gmail.com'])
        return redirect('product:index')
