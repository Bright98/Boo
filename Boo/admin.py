from django.contrib import admin

from .models import User, Category, CategoryItem

admin.site.register(User)
admin.site.register(Category)
admin.site.register(CategoryItem)