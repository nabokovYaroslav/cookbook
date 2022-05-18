<template>
  <div class="profile">
    <img :src="user.image" alt="user image" />
    <p v-if="isOwner">
      Почта:
      <i>
        <b>{{ user.email }}</b>
      </i>
    </p>
    <p>
      Имя пользователя:
      <i>
        <b>{{ user.user_name }}</b>
      </i>
    </p>
    <my-button
      style="margin-top: 15px"
      @click.native="onLogoutClick"
      v-if="isOwner && !isLogouting"
      >Выйти</my-button
    >
    <my-spinner
      style="margin-top: 15px"
      :size="40"
      v-if="isOwner && isLogouting"
    />
  </div>
</template>

<script>
import { mapActions } from "vuex";
import MyButton from "@/components/UI/MyButton";
import MySpinner from "@/components/MySpinner";
export default {
  components: {
    MyButton,
    MySpinner,
  },
  props: {
    user: {
      type: Object,
      required: true,
    },
    isOwner: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      isLogouting: false,
    };
  },
  methods: {
    ...mapActions("user", {
      logout: "logout",
    }),
    onLogoutClick() {
      this.isLogouting = true;
      this.logout()
        .then(() => {
          this.isLogouting = false;
        })
        .catch(() => {
          this.isLogouting = false;
        });
    },
  },
};
</script>

<style>
.profile {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile img {
  width: 140px;
  height: 140px;
  border-radius: 50%;
}

.profile .loader {
  display: flex;
  justify-content: center;
  padding: 50px 0;
}
</style>
