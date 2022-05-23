<template>
  <textarea :value="value" @input="$emit('input', $event.target.value)" />
</template>

<script>
export default {
  props: ["value"],
};
</script>

<style scoped>
textarea {
  width: 100%;
  padding: 10px 12px 10px 12px;
  border: 1px solid #ced4da;
  outline: 0;
  transition: 0.15s;
  font-size: 100%;
  resize: vertical;
}

textarea:focus {
  color: #222;
  border-color: #80bdff;
}
</style>
