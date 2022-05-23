<template>
  <div class="mobile-nav" :class="{ active: active }">
    <div class="link-wrapper">
      <ul>
        <mobile-menu-item
          v-for="category in categories"
          :key="category.id"
          :name="category.name"
          :id="category.id"
          @click.native="$emit('close')"
        />
      </ul>
    </div>
    <div class="layout" @click="$emit('close')"></div>
  </div>
</template>

<script>
import MobileMenuItem from "@/components/MobileMenuItem";

export default {
  components: {
    MobileMenuItem,
  },
  props: {
    categories: {
      type: Array,
      required: true,
    },
    active: {
      type: Boolean,
      required: true,
    },
  },
};
</script>

<style scoped>
.mobile-nav {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  visibility: hidden;
  z-index: 5;
}

.mobile-nav.active {
  visibility: visible;
}

.mobile-nav .link-wrapper {
  position: absolute;
  top: 0;
  bottom: 0;
  right: -100%;
  z-index: 1;
  min-width: 200px;
  overflow: hidden;
  transition: 0.3s;
}

.mobile-nav .link-wrapper ul {
  display: flex;
  flex-direction: column;
  transition: 0.3s;
  background-color: #35302d;
  height: 100%;
  overflow-y: auto;
}

.mobile-nav.active .link-wrapper {
  right: 0;
}

.mobile-nav .layout {
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 0;
  position: absolute;
  transition: 0.3s;
  visibility: hidden;
  opacity: 0;
}

.mobile-nav.active .layout {
  visibility: visible;
  opacity: 1;
}

ul::-webkit-scrollbar {
  width: 3px; /* ширина для вертикального скролла */
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
