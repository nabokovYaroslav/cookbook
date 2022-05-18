<template>
  <span
    class="spinner"
    :style="{
      '--border-width': borderWidth + 'px',
      '--border-indent-left': borderIndentLeft + 'px',
      '--border-indent-top': borderIndentTop + 'px',
      width: size + 'px',
      height: size + 'px',
    }"
  ></span>
</template>

<script>
export default {
  props: {
    size: {
      type: Number,
      default: 36,
    },
  },
  computed: {
    borderWidth() {
      return this.size / 6;
    },
    borderIndentLeft() {
      return this.borderWidth / 2;
    },
    borderIndentTop() {
      return -this.borderWidth;
    },
  },
};
</script>

<style scoped>
.spinner {
  display: block;
  position: relative;

  border: 2px solid rgba(0, 0, 0, 0.5);
  border-top-color: transparent;
  border-radius: 100%;

  animation: spin 1s infinite linear;
}

.spinner:after {
  content: "";
  display: block;
  width: 0;
  height: 0;
  position: absolute;
  top: var(--border-indent-top);
  left: var(--border-indent-left);

  border: var(--border-width) solid transparent;
  border-bottom-color: rgba(0, 0, 0, 0.5);

  transform: rotate(45deg);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
