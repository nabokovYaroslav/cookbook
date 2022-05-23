<template>
  <ul>
    <menu-item
      v-for="category in categories"
      :key="category.id"
      :name="category.name"
      :id="category.id"
    />
  </ul>
</template>

<script>
import MenuItem from "@/components/MenuItem";

export default {
  components: {
    MenuItem,
  },
  props: {
    categories: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
ul {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  overflow-y: hidden;
}

ul::-webkit-scrollbar {
  width: 24px; /* ширина для вертикального скролла */
  height: 3px; /* высота для горизонтального скролла */
  background-color: #cecece;
}

ul::-webkit-scrollbar-thumb {
  background-color: #ff4e00;
  border-radius: 9em;
  box-shadow: inset 1px 1px 10px #ff0000;
}

ul::-moz-scrollbar-button:decrement,
ul::-moz-scrollbar-button:increment,
ul::-webkit-scrollbar-button:decrement,
ul::-webkit-scrollbar-button:increment {
  width: 0px;
}
</style>
