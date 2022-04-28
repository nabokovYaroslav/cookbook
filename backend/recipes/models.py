from ast import arg
import os

from django.utils import timezone
from django.db import models

from users.models import User
from recipes.managers import StepManager
from utils.image import (change_resolution_of_image_in_memory, delete_images, create_adaptive_resolution_image, 
                         create_adaptive_format_image, create_tumbnail_image,) 
from utils.file import compare_images


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название категории")
    description = models.TextField(verbose_name="Описание категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Recipe(models.Model):
    def upload_to(self, file):
        name, ext = os.path.splitext(file)
        path = "images/recipes/"
        datetime = timezone.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        output_path = '{}{}-{}{}'.format(path, name, datetime, ext)
        return output_path

    name = models.CharField(max_length=255, verbose_name="Название рецепта")
    description = models.TextField(verbose_name="Описание рецепта")
    result = models.TextField(verbose_name="Описание результата")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    time = models.PositiveIntegerField(verbose_name="Время для приготовления", help_text="Время указывать в минутах")
    created_at = models.DateField(auto_now_add=True, verbose_name="Время публикации")
    colorie = models.PositiveIntegerField(verbose_name="Калории", help_text="На одну порцию")
    protein = models.PositiveIntegerField(verbose_name="Белки", help_text="На одну порцию")
    fat = models.PositiveIntegerField(verbose_name="Жиры", help_text="На одну порцию")
    carbohydrate = models.PositiveIntegerField(verbose_name="Углеводы", help_text="На одну порцию")
    count = models.PositiveSmallIntegerField(verbose_name="Количество порций", help_text="На скольких человек, расчитан рецепт")
    image = models.ImageField(verbose_name="Фотография", upload_to=upload_to)

    def save(self, *args, **kwargs):
        is_new_image = False
        try:
            instance = Recipe.objects.get(id=self.id)
        except Recipe.DoesNotExist:
            instance = None
        if instance is not None:
            if not compare_images(instance.image.path, self.image):
                delete_images(instance.image.path)
                self.image = change_resolution_of_image_in_memory(self.image)
                is_new_image = True
            else: 
                self.image = instance.image
        else:
            is_new_image = True
            self.image = change_resolution_of_image_in_memory(self.image)
        super().save(*args, **kwargs)
        if is_new_image:
            create_adaptive_resolution_image(self.image.path, formatting=True)
            create_adaptive_format_image(self.image.path)
            create_tumbnail_image(self.image.path, formatting=True)
        

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

class Unit(models.Model):
    name = models.CharField(max_length=255, verbose_name="Единицы измерения")
    short_name = models.CharField(max_length=255, verbose_name="Краткая форма единицы измерения")

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерений'

class Ingredient(models.Model):
    name = models.CharField(max_length=255, verbose_name="Ингридиент")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт", related_name="ingredients")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name="Единица измерения")
    value = models.DecimalField(max_digits=7, decimal_places=1, verbose_name="Значение")

    def __str__(self):
        return "Ингридиент {} к рецепту {}".format(self.name, str(self.recipe))

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

class Step(models.Model):
    def upload_to(self, file):
        name, ext = os.path.splitext(file)
        path = "images/recipes/"
        datetime = timezone.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        output_path = '{}{}-{}{}'.format(path, name, datetime, ext)
        return output_path

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт", related_name="steps")
    image = models.ImageField(verbose_name="Фотография", upload_to=upload_to)
    description = models.TextField(verbose_name="Описание шага")

    objects = StepManager()

    def save(self, *args, **kwargs):
        is_new_image = False
        try:
            instance = Step.objects.get(id=self.id)
        except Step.DoesNotExist:
            instance = None
        if instance is not None:
            if not compare_images(instance.image.path, self.image):
                delete_images(instance.image.path)
                self.image = change_resolution_of_image_in_memory(self.image)
                is_new_image = True
            else:
                self.image = instance.image.path
        else:
            is_new_image = True
            self.image = change_resolution_of_image_in_memory(self.image)
        super().save(*args, **kwargs)
        if is_new_image:
            create_adaptive_resolution_image(self.image.path, formatting=True)
            create_adaptive_format_image(self.image.path)

    def __str__(self):
        return "Шаг к рецепту {}".format(str(self.recipe))

    class Meta:
        verbose_name = 'Шаг'
        verbose_name_plural = 'Шаги'

class View(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    datetime = models.DateTimeField(auto_now_add=True, verbose_name="Дата просмотра")

    class Meta:
        unique_together = ["user", "recipe"]

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    reply_to = models.ForeignKey('self', related_name="answers", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Ответ к комментарию")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    text = models.TextField(verbose_name="Текст комментария")
    datetime = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")