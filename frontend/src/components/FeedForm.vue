<template>
  <div class="box">
    <form @submit.prevent="onFormSubmit">
      <div class="caption">Получай лучшие статьи на почту каждую неделю</div>
      <div class="form">
        <my-button
          v-if="!userIsLoading && !isSubscribing && !subscribed"
          type="submit"
          >Подписаться</my-button
        >
        <my-spinner v-if="isSubscribing || userIsLoading" :size="40" />
        <my-button
          v-if="!userIsLoading && !isSubscribing && subscribed"
          type="submit"
          >Отписаться</my-button
        >
      </div>
    </form>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import MyButton from "@/components/UI/MyButton";
import MySpinner from "@/components/MySpinner";
export default {
  components: {
    MyButton,
    MySpinner,
  },
  computed: {
    ...mapGetters("user", {
      isSubscribing: "isSubscribing",
      userIsLoading: "userIsLoading",
      authenticated: "authenticated",
      user: "user",
    }),
    subscribed() {
      return this.authenticated && this.user.is_subscriber;
    },
  },
  methods: {
    ...mapActions("user", {
      subscribe: "subscribe",
      unsubscribe: "unsubscribe",
    }),
    onFormSubmit() {
      if (!this.authenticated) this.$router.push({ name: "login" });
      if (this.subscribed) {
        this.unsubscribe();
      } else {
        this.subscribe();
      }
    },
  },
};
</script>

<style>
.box {
  margin: 50px 0;
  padding: 4px;
  background: url(@/assets/img/subscribe-bg.png);
}

.box form {
  padding: 30px;
  background: #f8f1fa;
}

.box form .caption {
  text-align: center;
  font-size: 1.1em;
  color: #222;
  line-height: 1.5;
}

.box form .form {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.box form .form input {
  padding: 0.6rem 1.5rem;
  margin: 0 0 0.6em;
  max-width: 100%;
  line-height: 1.5;
  color: #222;
  background-color: #fff;
  border: 1px solid #ced4da;
  transition: border-color 0.15s ease-in-out;
  font-size: 100%;
  outline: none;
}

.box form .form input:focus {
  border-color: #80bdff;
}
</style>
