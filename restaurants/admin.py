from django.contrib import admin
from .models import Restaurant, Menu, Category, MenuItem, Modifier
# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Modifier)
