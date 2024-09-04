from django.urls import path
from . import views

urlpatterns = [
    path('restaurants/', views.RestaurantListCreateView.as_view(), name='restaurant-list-create'),
    path('menus/', views.MenuListCreateView.as_view(), name='menu-list-create'),
    # Add URLs for other views (Category, MenuItem, Modifier)
]