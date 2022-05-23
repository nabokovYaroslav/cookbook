<template>
  <div class="form">
    <form @submit.prevent="onFormSubmit">
      <p>Вы действительно хотите удалить этот рецепт?</p>
      <div class="buttons" v-if="!formSubmitting">
        <my-button type="submit">Да</my-button>
        <my-button type="button" @click.native="onCloseClick">Нет</my-button>
      </div>
      <my-spinner v-else :size="40" style="margin-top: 15px" />
    </form>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import MyButton from "@/components/UI/MyButton";
import MySpinner from "@/components/MySpinner";
import { Recipe } from "@/api/recipe";
export default {
  components: {
    MyButton,
    MySpinner,
  },
  props: {
    recipeId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      formSubmitting: false,
    };
  },
  methods: {
    ...mapActions("user", {
      logout: "logout",
    }),
    onCloseClick() {
      this.$emit("close");
    },
    async onFormSubmit() {
      try {
        this.$emit("formSubmitting", true);
        this.formSubmitting = true;
        await Recipe.destroy(this.recipeId);
        this.$emit("delete", this.recipeId);
      } catch (error) {
        if (error.response) {
          const response = error.response;
          const status = response.status;
          if (status == 401) {
            await this.logout();
            this.$emit("close");
          } else if (status == 404) {
            this.$emit("delete", this.recipeId);
          }
        }
      } finally {
        this.$emit("formSubmitting", false);
        this.formSubmitting = false;
      }
    },
  },
};
</script>

<style scoped>
.form {
  padding: 20px;
}

.form form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form form p {
  font-size: 16px;
  font-weight: 600;
  text-align: center;
}

.form form .buttons {
  display: flex;
  justify-content: flex-end;
  margin-left: -15px;
  width: 100%;
  margin-top: 15px;
}

.form form .buttons > * {
  margin-left: 15px;
}
</style>
