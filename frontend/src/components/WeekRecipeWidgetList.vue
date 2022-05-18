<template>
  <recipe-widget-list :recipes="recipes">Рецепты недели</recipe-widget-list>
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
    const response = await Recipe.recipes_of_week_widget();
    this.recipes = response.data.results;
  },
};
</script>

<style></style>
