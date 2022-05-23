<template>
  <div class="dialog" v-if="show">
    <div class="dialog-content">
      <slot></slot>
    </div>
    <div class="layout" @click="hideDialog"></div>
  </div>
</template>

<script>
export default {
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    lock: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    hideDialog() {
      if (this.lock) return;
      this.$emit("hide", false);
    },
  },
};
</script>

<style scoped>
.dialog {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  display: flex;
  z-index: 2;
}
.dialog .dialog-content {
  margin: auto;
  background: #fff;
  border-radius: 12px;
  min-height: 50px;
  min-width: 300px;
  z-index: 1;
}

.dialog .layout {
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 0;
  position: absolute;
}
</style>
