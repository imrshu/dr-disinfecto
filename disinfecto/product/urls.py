from django.urls import path
from .views import *
from django.contrib.auth.views import (login, logout, password_reset, password_reset_done,
password_reset_confirm, password_reset_complete
)

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
    path('services', getServices, name = 'services'),
    path('payment', payment, name='payment'),
    # path('product/<product_id>/', productorder, name='productorder'),
    path('feedback', feedback, name='feedback'),
    path('success/', success, name='success'),
    path('cart', addtocart, name='addtocart'),
    path('showcart', showcart, name='showcart'),
    path('refund_policy', refund_policy, name='refund_policy'),
    path('terms_of_condition', terms_of_condition, name='terms_of_condition'),
    path('privacy_policy', privacy_policy, name='privacy_policy'),
]
