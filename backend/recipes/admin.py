from atexit import register
from django.contrib import admin

from recipes.models import Category, Unit, Recipe, Subscriber

admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Recipe)
admin.site.register(Subscriber)