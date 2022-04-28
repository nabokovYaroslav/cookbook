from django.apps import AppConfig


class RecipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'
    verbose_name = "Рецепты"

    def ready(self):
        from recipes.signals import recipe_delete_images, step_delete_images, step_update_image, step_created
        return super().ready()