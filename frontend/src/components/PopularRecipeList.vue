<template>
  <recipe-list :recipes="recipes" class="recipe-list" />
</template>

<script>
import RecipeList from "@/components/RecipeList";
import { Recipe } from "@/api/recipe";
export default {
  components: {
    RecipeList,
  },
  data() {
    return {
      recipes: [],
    };
  },
  async created() {
    const response = await Recipe.popular_recipes();
    this.recipes = response.data.results;
  },
};
</script>

<style scoped>
.recipe-list {
  margin-top: 30px;
}
</style>
