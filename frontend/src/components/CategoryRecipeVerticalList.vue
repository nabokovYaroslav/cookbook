<template>
  <recipe-vertical-list :recipes="recipes" />
</template>

<script>
import { RecipeCategory } from "@/api/recipeCategory";
import RecipeVerticalList from "@/components/RecipeVerticalList";
export default {
  components: {
    RecipeVerticalList,
  },
  data() {
    return {
      recipes: [],
    };
  },
  async created() {
    const response = await RecipeCategory.list(this.$route.params.id);
    this.recipes = response.data.results;
  },
};
</script>

<style></style>
