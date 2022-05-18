<template>
  <div class="widget">
    <div class="widget-header"><slot></slot></div>
    <div class="widget-content">
      <recipe-widget-item
        v-for="recipe in recipes"
        :key="recipe.id"
        :recipe="recipe"
      />
    </div>
  </div>
</template>

<script>
import RecipeWidgetItem from "@/components/RecipeWidgetItem";

export default {
  props: {
    recipes: {
      type: Array,
      required: true,
    },
  },
  components: {
    RecipeWidgetItem,
  },
};
</script>

<style scoped>
.widget {
  margin-bottom: 50px;
}

.widget .widget-header {
  text-transform: uppercase;
  font-weight: 700;
  font-size: 16px;
  line-height: 1.5;
}

.widget .widget-header::after {
  content: "";
  position: relative;
  display: inline-block;
  top: -2px;
  width: 12px;
  height: 3px;
  margin-left: 10px;
  vertical-align: middle;
  background: #ff4e00;
}
</style>
