<template>
  <form @submit.prevent="$emit('formSubmit')">
    <my-input
      @input="$emit('searchChange', $event)"
      :value="search"
      style="padding-right: 15px"
    />
    <button type="submit" :disabled="search === ''">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        class="bi bi-search"
        viewBox="0 0 16 16"
      >
        <path
          d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"
        />
      </svg>
    </button>
  </form>
</template>

<script>
import MyInput from "@/components/UI/MyInput";
export default {
  components: {
    MyInput,
  },
  props: {
    search: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
form {
  position: relative;
}

form button svg {
  width: 16px;
  height: 16px;
}

form button {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  border: none;
  background: 0 0;
  cursor: pointer;
  opacity: 0.6;
  transition: all 0.3s;
  height: 100%;
  width: 40px;
}

form button:hover {
  opacity: 1;
}
</style>
