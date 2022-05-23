<template>
  <form @submit.prevent="onFormSubmit">
    <my-textarea
      placeholder="Комментарий"
      v-model="text.value"
      rows="7"
      @input.native="text.valid = text.value !== ''"
    />
    <my-button
      v-if="!isFormSubmitting"
      style="align-self: flex-end; margin-top: 15px"
      :disabled="!formIsValid"
      >Отправить</my-button
    >
    <my-spinner
      :size="40"
      v-else
      style="align-self: flex-end; margin-top: 15px"
    />
  </form>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import MyTextarea from "@/components/UI/MyTextarea";
import MyButton from "@/components/UI/MyButton";
import MySpinner from "@/components/MySpinner";
import { Comment } from "@/api/comment";

export default {
  components: {
    MyTextarea,
    MyButton,
    MySpinner,
  },
  props: {
    recipeId: {
      type: [Number, String],
      required: true,
    },
  },
  data() {
    return {
      text: {
        value: "",
        valid: false,
      },
      isFormSubmitting: false,
    };
  },
  computed: {
    formIsValid() {
      return this.text.valid;
    },
    ...mapGetters("user", {
      user: "user",
    }),
  },
  methods: {
    ...mapActions("user", {
      logout: "logout",
    }),
    async onFormSubmit() {
      try {
        this.isFormSubmitting = true;
        const response = await Comment.create(
          this.recipeId,
          this.user.user,
          null,
          this.text.value
        );
        this.$emit("commentCreated", response.data);
        this.text.value = "";
        this.text.valid = false;
      } catch (error) {
        if (error.response) {
          const response = error.response;
          const status = response.status;
          if (status == 401) {
            await this.logout();
          }
        }
      } finally {
        this.isFormSubmitting = false;
      }
    },
  },
};
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

form button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
