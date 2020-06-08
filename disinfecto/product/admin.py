from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Feedback)

admin.site.site_header = "Dr Disinfecto"
admin.site.site_title = "DR DISINFECTO ADMIN"
admin.site.index_title = "WELCOME TO DR DISINFECTO"