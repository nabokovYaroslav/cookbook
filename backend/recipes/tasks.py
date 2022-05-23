from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone
from django.core.mail import send_mail

from config.celery import app
from recipes.models import Subscriber, Recipe


@app.task
def send_recipes_of_week_to_subscribers():
    recipes_of_week = (
                Recipe
                .objects
                .annotate(views_count=Count("views", filter=Q(views__datetime__range=(timezone.now() - timedelta(days=7), timezone.now())), distinct=True))
                .order_by("-views_count")
                )[:6]
    subscribers = Subscriber.objects.select_related("user")
    emails = [subscriber.user.email for subscriber in subscribers]
    base_link = "http://localhost:8080/categories/{category_id}/recipes/{recipe_id}"
    links = [base_link.format(category_id=recipe.category_id, recipe_id=recipe.id) for recipe in recipes_of_week]
    send_mail(
              subject="Рецепты недели",
              message='''Здравствуйте, мы подготовили для вас подборку рецептов, которые были самыми просматриваемыми за неделю!\n{links}'''.format(links="\n".join(links)),
              from_email="romanbudkevich@gmail.com",
              recipient_list=emails,
              fail_silently=False,
              )