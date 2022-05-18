<template>
  <button><slot></slot></button>
</template>

<script>
export default {};
</script>

<style scoped>
button {
  background: #ff4e00;
  display: inline-block;
  font-weight: 400;
  text-align: center;
  border: 2px solid #ff4e00;
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  line-height: 1.5;
  color: #fff;
  cursor: pointer;
  transition: 0.3s;
}

button:hover {
  color: #ff4e00;
  background-color: #fff;
}
</style>
