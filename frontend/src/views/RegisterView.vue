<template>
  <main>
    <register-form class="register-form" />
  </main>
</template>

<script>
import RegisterForm from "@/components/RegisterForm";

export default {
  components: {
    RegisterForm,
  },
};
</script>

<style scoped>
main {
  padding: 50px 0;
}

.register-form {
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}
</style>
