<template>
  <li>
    <router-link :to="{ name: 'category', params: { id: id } }">{{
      name
    }}</router-link>
  </li>
</template>

<script>
export default {
  props: {
    name: {
      type: String,
      required: true,
    },
    id: {
      type: Number,
      required: true,
    },
  },
};
</script>

<style scoped>
li {
  white-space: nowrap;
  margin-left: 15px;
}

li:first-child {
  margin-left: 0;
}

li a {
  padding: 18px 5px;
  display: block;
  position: relative;
  text-transform: uppercase;
  color: #222;
  font-size: 0.95em;
  font-weight: 700;
  transition: all 0.3s;
}

li a::before {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 2px;
  background: #ff4e00;
  opacity: 0;
  transition: all 0.3s;
  transform: translateY(-10px) translateZ(0);
}

li a:hover::before {
  transform: translateY(0) translateZ(0);
  opacity: 1;
}
</style>
