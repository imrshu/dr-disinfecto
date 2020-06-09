from django.urls import path
from .views import *
from django.contrib.auth.views import login, logout


app_name = 'product'
urlpatterns = [
    path('', index, name = 'index'),
    path('complaint', complaint, name = 'complaint'),
    path('inquiry', inquiry, name = 'inquiry'),
    path('allproducts', getAllProducts, name='allproducts'),
    path('reviews', giveReview, name='giveReview'),
    path('login', login, name = 'login'),
    path('signup', signup, name = 'signup'),
    path('logout', logout, {'next_page': '/'}, name = 'logout'),
    path('home', home, name = 'home'),
    path('product/<product_id>/', productorder, name='productorder'),
    path('feedback', feedback, name='feedback'),
    path('success/', success, name='success')
]
