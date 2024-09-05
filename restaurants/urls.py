from django.urls import path
from . import views

urlpatterns = [
    path('restaurants/', views.RestaurantListCreateView.as_view(),
         name='restaurant-list-create'),
    path('menus/', views.MenuListCreateView.as_view(), name='menu-list-create'),
    path('categories/', views.CategoryListCreateView.as_view(),
         name='category-list-create'),
    path('menu-items/', views.MenuItemListCreateView.as_view(),
         name='menu-item-list-create'),
    path('modifiers/', views.ModifierListCreateView.as_view(),
         name='modifier-list-create'),
]
