<template>
  <div class="row recipes">
    <div
      class="col-12 col-sm-6 col-lg-4"
      v-for="recipe in recipes"
      :key="recipe.id"
    >
      <recipe-item :recipe="recipe" />
    </div>
  </div>
</template>

<script>
import RecipeItem from "@/components/RecipeItem";
export default {
  components: {
    RecipeItem,
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
