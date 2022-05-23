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
  position: relative;
  border-bottom: solid 1px #3c3735;
}

li a {
  display: block;
  position: relative;
  z-index: 1;
  transition: 0.35s ease color;
  padding: 1.1em 10px;
  color: #dfdbd9;
  text-align: center;
}

li a:hover {
  color: #fff;
}

li a:hover::before {
  left: -5px;
}

li a::before {
  content: "";
  display: block;
  z-index: -1;
  position: absolute;
  left: calc(-100% - 5px);
  top: 0;
  width: 100%;
  height: 100%;
  border-right: solid 5px #df4500;
  background: #3c3735;
  transition: 0.35s ease left;
}
</style>
