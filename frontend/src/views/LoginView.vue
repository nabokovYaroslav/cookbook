<template>
  <main>
    <login-form class="login-form" />
  </main>
</template>

<script>
import LoginForm from "@/components/LoginForm";

export default {
  components: {
    LoginForm,
  },
};
</script>

<style scoped>
main {
  padding: 50px 0;
}

.login-form {
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}
</style>
