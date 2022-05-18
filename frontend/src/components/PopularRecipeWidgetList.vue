<template>
  <recipe-widget-list :recipes="recipes">Популярные рецепты</recipe-widget-list>
</template>

<script>
import RecipeWidgetList from "@/components/RecipeWidgetList";
import { Recipe } from "@/api/recipe";

export default {
  components: {
    RecipeWidgetList,
  },
  data() {
    return {
      recipes: [],
    };
  },
  async created() {
    const response = await Recipe.popular_recipes_widget();
    this.recipes = response.data.results;
  },
};
</script>

<style></style>
