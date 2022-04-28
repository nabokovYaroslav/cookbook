from django.db import transaction
from rest_framework import serializers

from recipes.models import Recipe, Ingredient, Step, Comment, View
from recipes.fields import ImageField, RecursiveField, TumbnailImageField
from utils.file import compare_images


class RecipeListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(read_only=True, source='category.name')
    image = ImageField()
    views_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('name', 'description', 'category', 'category_name', 'time', 'image', 'count',
                  'views_count', 'comments_count',
                  )

class IgridientSerializer(serializers.ModelSerializer):
    unit_name = serializers.CharField(read_only=True, source='unit.name')
    unit_short_name = serializers.CharField(read_only=True, source="unit.short_name")

    class Meta:
        model = Ingredient
        fields = ("id","name", "recipe", "unit", "unit_name", "unit_short_name", "value")

class StepSerializer(serializers.ModelSerializer):
    image = ImageField()

    class Meta:
        model = Step
        fields = '__all__'

class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    ingredients = IgridientSerializer(many=True, required=True)
    steps = StepSerializer(many=True, required=True)

    def validate_ingredients(self, ingredients):
        for ingredient in ingredients:
            id = ingredient.get("id", None)
            if id is not None:
                recipe_id = self.instance.id
                try:
                    Ingredient.objects.get(id=id, recipe_id=recipe_id)
                except Ingredient.DoesNotExist:
                    raise (
                           serializers
                           .ValidationError("Recipe with id={} has no Ingredient with id={}"
                           .format(recipe_id, id))
                           )

    def validate_steps(self, steps):
        for step in steps:
            id = step.get("id", None)
            if id is not None:
                recipe_id = self.instance.id
                try:
                    Step.objects.get(id=id, recipe_id=recipe_id)
                except Step.DoesNotExist:
                    raise (
                           serializers
                           .ValidationError("Recipe with id={} has no Step with id={}"
                           .format(recipe_id, id))
                           )

    def create(self, validated_data):
        ingredient_data = validated_data.pop('ingredients', [])
        step_data = validated_data.pop('steps', [])
        with transaction.atomic():
            recipe = Recipe.objects.create(**validated_data)
            
            ingredient_data = [{"recipe_id": recipe.id, **ingredient} for ingredient in ingredient_data]
            ingrident_objects = [Ingredient(**ingredient) for ingredient in ingredient_data]
            
            step_data = [{"recipe_id": recipe.id, **step} for step in step_data]
            step_objects = [Step(**step) for step in step_data]

            if ingrident_objects:
                Ingredient.objects.bulk_create(ingrident_objects)
            if step_objects:   
                Step.objects.bulk_create(step_objects)    
        return recipe

    def update(self, instance, validated_data):
        ingredient_data = validated_data.pop('ingredients', [])
        step_data = validated_data.pop('steps', [])

        ingredients = instance.ingredients.all()
        steps = instance.steps.all()
        
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.result = validated_data.get('result', instance.result)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.time = validated_data.get('time', instance.time)
        instance.colorie = validated_data.get('colorie', instance.colorie)
        instance.protein = validated_data.get('protein', instance.protein)
        instance.fat = validated_data.get('fat', instance.fat)
        instance.carbohydrate = validated_data.get('carbohydrate', instance.carbohydrate)
        instance.count = validated_data.get('count', instance.count)
        instance.image = validated_data.get('image', instance.image)

        ingredient_data = [
                            {"recipe_id": instance.id, **ingredient} 
                            for ingredient in ingredient_data 
                            if not "recipe_id" in ingredient
                            ]
            
        ingredient_objects_to_create = [
                                        Ingredient(**ingredient) 
                                        for ingredient in ingredient_data 
                                        if ingredient.get('id', None) is None
                                        ]
        ingredient_objects_to_update = []
        ingredient_objects_to_delete = []
        for ingredient in ingredients:
            new_data = next((item for item in ingredient_data if item.get("id", None) == ingredient.id), None)
            if new_data is not None:
                ingredient.name = new_data.get("name", ingredient.name)
                ingredient.recipe_id = new_data.get("recipe_id", ingredient.recipe_id)
                ingredient.unit_id = new_data.get("unit_id", ingredient.unit_id)
                ingredient.value = new_data.get("value", ingredient.value)
                ingredient_objects_to_update.append(ingredient)
            else:
                ingredient_objects_to_delete.append(ingredient)

        if step_data is not None:
            step_data = [
                         {"recipe_id": instance.id, **step}
                         for step in step_data
                         if not "recipe_id" in step
                         ]

        step_objects_to_create = [
                                  Step(**step) 
                                  for step in step_data 
                                  if step.get('id', None) is None
                                  ]
        step_objects_to_update = []
        # Objects whose picture has changed
        # Since we handle saving the image in the .save() method, 
        # we have to handle this ourselves, as the .save() method 
        # is not called on bulk_create or bulk_update.
        step_objects_image_updated = []
        step_objects_to_delete = []
        for step in steps:
            new_data = next((item for item in step_data if item.get("id", None) == step.id), None)
            if new_data is not None:
                step.recipe_id = new_data.get("recipe_id", step.recipe_id)
                step.image = new_data.get("image", step.image)
                step.description = new_data.get("description", step.description)
                step_objects_to_update.append(step)
            else:
                step_objects_to_delete.append(step)
        
        with transaction.atomic():
            instance.save()

            Ingredient.objects.bulk_create(ingredient_objects_to_create, batch_size=None, ignore_conflicts=False)
            if ingredients is not None:
                Ingredient.objects.bulk_update(ingredient_objects_to_update, batch_size=None, fields=["name", "recipe_id", "unit_id", "value"])
                for ingredient in ingredient_objects_to_delete:
                    ingredient.delete()

            Step.objects.bulk_create(step_objects_to_create, batch_size=None, ignore_conflicts=False)
            if steps is not None:
                Step.objects.bulk_update(step_objects_to_update, batch_size=None, fields=["recipe_id", "image", "description"], step_objects_image_updated=step_objects_image_updated)
                for step in step_objects_to_delete:
                    step.delete()
        return instance
            
    class Meta:
        model = Recipe
        fields = (
                  'id', 'name', 'description', 'result', 'category', 'user', 'time', 'colorie', 
                  'protein', 'fat', 'carbohydrate', 'count', 'image', 'ingredients', 'steps',
                  )

class RecipeRetrieveSerializer(serializers.ModelSerializer):
    ingredients = IgridientSerializer(many=True)
    steps = StepSerializer(many=True)
    category_name = serializers.CharField(read_only=True, source='category.name')
    user_name = serializers.CharField(read_only=True, source='user.user_name')
    image = ImageField()
    views_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Recipe
        fields = (
                  'name', 'description', 'result', 'category', 'user', 'time', 'colorie', 'created_at', 
                  'protein', 'fat', 'carbohydrate', 'count', 'image', 'ingredients', 'steps', 'views_count',
                  'comments_count', 'category_name', 'user_name'
                  )

class RecipeDestroySerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"

class CommentListRetrieveSerializer(serializers.ModelSerializer):
    answers = RecursiveField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ("user", "reply_to", "recipe", "text", "datetime", "answers")

class CommentCreateUpdateDestroySerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"

class ViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = View
        fields = "__all__"

class RecipeWidgetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(read_only=True, source='category.name')
    image = TumbnailImageField()
    
    class Meta:
        model = Recipe
        fields = ("name", "time", "category", "category_name", "count", "image")

class RecipeSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ("name", "time", "category", "category_name", "count", "image")