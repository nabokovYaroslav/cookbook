from django.contrib import admin

from recipes.models import Category, Unit, Recipe

admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Recipe)