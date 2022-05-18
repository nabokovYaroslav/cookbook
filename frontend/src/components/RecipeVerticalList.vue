<template>
  <div class="row recipes">
    <recipe-vertical-item
      v-for="recipe in recipes"
      :key="recipe.id"
      :recipe="recipe"
    />
  </div>
</template>

<script>
import RecipeVerticalItem from "@/components/RecipeVerticalItem";
export default {
  components: {
    RecipeVerticalItem,
  },
  props: {
    recipes: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
.recipes {
  margin-bottom: -48px;
}
</style>
