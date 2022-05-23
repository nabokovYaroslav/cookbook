from django.db import transaction
from rest_framework import serializers

from recipes.models import Recipe, Ingredient, Step, Comment, View, Category, Unit
from recipes.fields import ImageField, RecursiveField, TumbnailImageField, CustomBase64ImageField, AdaptiveImage
from users.api.serializers import UserBasicSerializer


class RecipeListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(read_only=True, source='category.name')
    image = ImageField()
    views_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'category', 'category_name', 'time', 'image', 'count',
                  'views_count', 'comments_count',
                  )

class IngredientCreateSerializer(serializers.ModelSerializer):
    unit_name = serializers.CharField(read_only=True, source='unit.name')
    unit_short_name = serializers.CharField(read_only=True, source="unit.short_name")

    class Meta:
        model = Ingredient
        fields = ("id", "name", "unit", "unit_name", "unit_short_name", "value")

class IngredientUpdateSerializer(serializers.ModelSerializer):
    unit_name = serializers.CharField(read_only=True, source='unit.name')
    unit_short_name = serializers.CharField(read_only=True, source="unit.short_name")

    def to_internal_value(self, data):
        obj = super().to_internal_value(data)
        obj["id"] = data.get("id")
        return obj

    class Meta:
        model = Ingredient
        fields = ("id", "name", "unit", "unit_name", "unit_short_name", "value")
        extra_kwargs = {
            "id": {"allow_null": True}
        }

class IngredientSerializer(serializers.ModelSerializer):
    unit_short_name = serializers.CharField(read_only=True, source="unit.short_name")
    
    class Meta:
        model = Ingredient
        fields = ("id", "name", "value", "recipe", "unit", "unit_short_name")

class StepSerializer(serializers.ModelSerializer):
    image = ImageField()

    class Meta:
        model = Step
        fields = '__all__'

class StepCreateSerializer(serializers.ModelSerializer):
    image = CustomBase64ImageField()

    class Meta:
        model = Step
        fields = ("id", "image", "description")

class StepUpdateSerializer(serializers.ModelSerializer):
    image = CustomBase64ImageField()

    def to_internal_value(self, data):
        obj = super().to_internal_value(data)
        obj["id"] = data.get("id")
        return obj

    class Meta:
        model = Step
        fields = ("id", "image", "description")
        extra_kwargs = {
            "id": {"allow_null": True}
        }
        

class RecipeCreateSerialzer(serializers.ModelSerializer):
    ingredients = IngredientCreateSerializer(many=True, required=True)
    steps = StepCreateSerializer(many=True, required=True)
    image = CustomBase64ImageField()

    def create(self, validated_data):
        ingredient_data = validated_data.pop('ingredients', [])
        if ingredient_data is None:
            ingredient_data = []
        step_data = validated_data.pop('steps', [])
        if step_data is None:
            step_data = []
        with transaction.atomic():
            recipe = Recipe.objects.create(**validated_data)
            
            ingredient_data = [{"recipe_id": recipe.id, **ingredient} for ingredient in ingredient_data]
            ingrident_objects = [Ingredient(**ingredient) for ingredient in ingredient_data]
            
            step_data = [{"recipe_id": recipe.id, **step} for step in step_data]
            step_objects = [Step(**step) for step in step_data]

            if ingrident_objects:
                Ingredient.objects.bulk_create(ingrident_objects)
            if step_objects:   
                Step.objects.bulk_create(step_objects, batch_size=None, ignore_conflicts=False)    
        return recipe

    class Meta:
        model = Recipe
        fields = (
                  'id', 'name', 'description', 'result', 'category', 'user', 'time', 'colorie', 
                  'protein', 'fat', 'carbohydrate', 'count', 'image', 'ingredients', 'steps',
                  )

class RecipeUpdateSerializer(serializers.ModelSerializer):
    ingredients = IngredientUpdateSerializer(many=True, required=True)
    steps = StepUpdateSerializer(many=True, required=True)
    image = CustomBase64ImageField()

    def validate_ingredients(self, ingredients):
        for ingredient in ingredients:    
            id = ingredient["id"]
            if id is not None:
                try:
                    Ingredient.objects.get(id=id)
                except Ingredient.DoesNotExist:
                    raise (
                            serializers
                            .ValidationError("Ingredient with id={} does not exist"
                            .format(id))
                            )
                try:
                    recipe_id = self.instance.id
                    Ingredient.objects.get(id=id, recipe_id=recipe_id)
                except Ingredient.DoesNotExist:
                    raise (
                            serializers
                            .ValidationError("Recipe with id={} has no Ingredient with id={}"
                            .format(recipe_id, id))
                            )
        return ingredients

    def validate_steps(self, steps):
        for step in steps:
            id = step["id"]
            if id is not None:
                try:
                    Step.objects.get(id=id)
                except Step.DoesNotExist:
                    raise (
                            serializers
                            .ValidationError("Step with id={} does not exist"
                            .format(id))
                            )
                recipe_id = self.instance.id
                try:
                    Step.objects.get(id=id, recipe_id=recipe_id)
                except Step.DoesNotExist:
                    raise (
                           serializers
                           .ValidationError("Recipe with id={} has no Step with id={}"
                           .format(recipe_id, id))
                           )
        return steps

    def update(self, instance, validated_data):
        ingredient_data = validated_data.pop('ingredients', [])
        if ingredient_data is None:
            ingredient_data = []
        step_data = validated_data.pop('steps', [])
        if step_data is None:
            step_data = []

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
                            ]
            
        ingredient_objects_to_create = [
                                        Ingredient(**ingredient) 
                                        for ingredient in ingredient_data 
                                        if ingredient["id"] is None
                                        ]
        ingredient_objects_to_update = []
        ingredient_objects_to_delete = []
        for ingredient in ingredients:
            new_data = next((item for item in ingredient_data if item["id"] == ingredient.id), None)
            if new_data is not None:
                ingredient.name = new_data.get("name", ingredient.name)
                ingredient.recipe_id = new_data.get("recipe_id", ingredient.recipe_id)
                ingredient.unit_id = new_data.get("unit_id", ingredient.unit_id)
                ingredient.value = new_data.get("value", ingredient.value)
                ingredient_objects_to_update.append(ingredient)
            else:
                ingredient_objects_to_delete.append(ingredient)

        step_data = [
                     {"recipe_id": instance.id, **step}
                     for step in step_data
                     ]

        step_objects_to_create = [
                                  Step(**step) 
                                  for step in step_data 
                                  if step["id"] is None
                                  ]
        step_objects_to_update = []
        step_objects_to_delete = []
        for step in steps:
            new_data = next((item for item in step_data if item["id"] == step.id), None)
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
                for step in step_objects_to_update:
                    step.save()
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
    ingredients = IngredientSerializer(many=True)
    steps = StepSerializer(many=True)
    category_name = serializers.CharField(read_only=True, source='category.name')
    user_name = serializers.CharField(read_only=True, source='user.user_name')
    image = ImageField()
    views_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Recipe
        fields = (
                  'id', 'name', 'description', 'result', 'category', 'user', 'time', 'colorie', 'created_at', 
                  'protein', 'fat', 'carbohydrate', 'count', 'image', 'ingredients', 'steps', 'views_count',
                  'comments_count', 'category_name', 'user_name'
                  )

class RecipeDestroySerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"

class CommentListSerializer(serializers.ModelSerializer):
    answers = RecursiveField(many=True, read_only=True)
    user = UserBasicSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ("id", "user", "reply_to", "recipe", "text", "datetime", "answers")

class CommentCreateDestroySerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"

class ViewSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = View
        fields = "__all__"

class RecipeWidgetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(read_only=True, source='category.name')
    image = TumbnailImageField()
    
    class Meta:
        model = Recipe
        fields = ("id", "name", "time", "category", "category_name", "count", "image")

class RecipeWidgetSearchSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(read_only=True, source='category.name')
    image = TumbnailImageField()
    class Meta:
        model = Recipe
        fields = ("id", "name", "category", "category_name", "image")

class RecipeSearchSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(read_only=True, source='category.name')
    image = ImageField()
    views_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'category', 'category_name', 'time', 'image', 'count',
                  'views_count', 'comments_count',
                  )

class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("id", "name",)

class CategoryRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

class RecipeRandomSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(read_only=True, source="category.name") 
    image = AdaptiveImage()
    
    class Meta:
        model = Recipe
        fields = ("id", "category", "category_name", "image", "name", "description")

class IngredientEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ("id", "name", "unit", "value")

class StepEditSerializer(serializers.ModelSerializer):
    image = CustomBase64ImageField(represent_in_base64=True)

    class Meta:
        model = Step
        fields = ("id", "image", "description",)

class RecipeEditSerializer(serializers.ModelSerializer):
    ingredients = IngredientEditSerializer(many=True)
    steps = StepEditSerializer(many=True)
    image = CustomBase64ImageField(represent_in_base64=True)

    class Meta:
        model = Recipe
        fields = (
                  'id', 'name', 'description', 'result', 'category', 'time', 'colorie', 
                  'protein', 'fat', 'carbohydrate', 'count', 'image', 'ingredients', 'steps',
                  )

class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        fields = "__all__"   