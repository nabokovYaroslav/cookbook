<template>
  <div>
    <h1 class="category-title">{{ category.name }}</h1>
    <div class="category-description">
      <p>{{ category.description }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    category: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style>
.category-title {
  font-size: 40px;
}

.category-description {
  margin-top: 40px;
}

.category-description p:not(:first-child) {
  margin-top: 24px;
}

.category-description p {
  font-size: 16px;
  line-height: 1.5;
  color: #222;
}
</style>
