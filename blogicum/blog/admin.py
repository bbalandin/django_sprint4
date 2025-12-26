from django.contrib import admin

# Из модуля models импортируем модель Category...
from .models import Category, Location, Post, Comments

# ...и регистрируем её в админке:
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Post)
admin.site.register(Comments)
