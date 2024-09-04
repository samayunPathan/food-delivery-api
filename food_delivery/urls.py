
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('users.urls')),
    path('restaurants/',include('restaurants.urls')),
    path('orders/',include('orders.urls')),
]
