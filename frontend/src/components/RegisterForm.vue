<template>
  <div class="register">
    <h1>Зарегистрироваться</h1>
    <form @submit.prevent="onFormSubmit">
      <div class="main-error" :class="{ active: error.isVisible }">
        {{ error.message }}
      </div>
      <div class="form-group">
        <span class="error" :class="{ active: username.error.isVisible }">{{
          username.error.message
        }}</span>
        <my-input
          placeholder="Имя пользовтеля"
          v-model="username.value"
          @input="onUsernameInput"
        />
      </div>
      <div class="form-group">
        <span class="error" :class="{ active: email.error.isVisible }">{{
          email.error.message
        }}</span>
        <my-input
          placeholder="E-mail"
          v-model="email.value"
          @input="onEmailInput"
        />
      </div>
      <div class="form-group">
        <span class="error" :class="{ active: password.error.isVisible }">{{
          password.error.message
        }}</span>
        <my-input
          placeholder="Пароль"
          v-model="password.value"
          @input="onPasswordInput"
          type="password"
        />
      </div>
      <div class="form-group">
        <span class="error" :class="{ active: passwordCopy.error.isVisible }">{{
          passwordCopy.error.message
        }}</span>
        <my-input
          placeholder="Повторите пароль"
          v-model="passwordCopy.value"
          @input="onPasswordCopyInput"
          type="password"
        />
      </div>
      <my-spinner v-if="formSubmitting" style="margin-top: 15px" :size="40" />
      <my-button v-else :disabled="!formIsValid">Зарегистрироваться</my-button>
    </form>
    <div class="additional">
      <p>Уже есть аккаунт?</p>
      <router-link :to="{ name: 'login' }">Войдите!</router-link>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import MyInput from "@/components/UI/MyInput";
import MyButton from "@/components/UI/MyButton";
import MySpinner from "@/components/MySpinner";

export default {
  components: {
    MyInput,
    MyButton,
    MySpinner,
  },
  data() {
    return {
      username: {
        value: "",
        error: {
          isVisible: false,
          message: "",
        },
        valid: false,
      },
      email: {
        value: "",
        error: {
          isVisible: false,
          message: "",
        },
        valid: false,
      },
      password: {
        value: "",
        error: {
          isVisible: false,
          message: "",
        },
        valid: false,
      },
      passwordCopy: {
        value: "",
        error: {
          isVisible: false,
          message: "",
        },
        valid: false,
      },
      formSubmitting: false,
      error: {
        isVisible: false,
        message: "",
      },
    };
  },
  methods: {
    ...mapActions("user", {
      register: "register",
    }),

    async onFormSubmit() {
      try {
        this.formSubmitting = true;
        await this.register({
          email: this.email.value,
          username: this.username.value,
          password: this.password.value,
        });
        this.$router.push({ name: "login" });
      } catch (error) {
        if (error.response) {
          const response = error.response;
          const status = response.status;
          if (status === 401) {
            this.error.message = response.data.detail;
            this.error.isVisible = true;
          } else if (status === 400) {
            if (response.data.user_name) {
              this.username.valid = false;
              this.username.error.message = response.data.user_name.join("\n");
              this.username.error.isVisible = true;
            }
            if (response.data.email) {
              this.email.valid = false;
              this.email.error.message = response.data.email.join("\n");
              this.email.error.isVisible = true;
            }
            if (response.data.password) {
              this.password.valid = false;
              this.password.error.message = response.data.password.join("\n");
              this.password.error.isVisible = true;
            }
            this.error.message = "Исправьте ошибки ниже";
            this.error.isVisible = true;
          }
        }
      } finally {
        this.formSubmitting = false;
      }
    },
    onUsernameInput() {
      this.error.isVisible = false;
      if (this.username.value.length == 0) {
        this.username.valid = false;
        this.username.error.message = "Обязательное поле";
        this.username.error.isVisible = true;
        return;
      }
      if (this.username.value.length > 255) {
        this.username.valid = false;
        this.username.error.message =
          "Имя пользователя не может быть больше 255 символов";
        this.username.error.isVisible = true;
        return;
      }
      this.username.valid = true;
      this.username.error.message = "";
      this.username.error.isVisible = false;
    },
    onEmailInput() {
      this.error.isVisible = false;
      if (this.email.value.length == 0) {
        this.email.valid = false;
        this.email.error.message = "Обязательное поле";
        this.email.error.isVisible = true;
        return;
      }
      if (this.email.value.length > 254) {
        this.email.valid = false;
        this.email.error.message =
          "Имя почты не может быть больше 254 символов";
        this.email.error.isVisible = true;
        return;
      }
      if (!this.email.value.includes("@")) {
        this.email.valid = false;
        this.email.error.message = "Невалидное имя почты";
        this.email.error.isVisible = true;
        return;
      }
      this.email.valid = true;
      this.email.error.message = "";
      this.email.error.isVisible = false;
    },
    onPasswordInput() {
      this.error.isVisible = false;
      if (this.password.value.length == 0) {
        this.password.valid = false;
        this.password.error.message = "Обязательное поле";
        this.password.error.isVisible = true;
        return;
      }
      if (this.password.value.length > 255) {
        this.password.valid = false;
        this.password.error.message =
          "Пароль не может быть больше 255 символов";
        this.password.error.isVisible = true;
        return;
      }
      this.password.valid = true;
      this.password.error.message = "";
      this.password.error.isVisible = false;
    },
    onPasswordCopyInput() {
      this.error.isVisible = false;
      if (this.passwordCopy.value.length == 0) {
        this.passwordCopy.valid = false;
        this.passwordCopy.error.message = "Обязательное поле";
        this.passwordCopy.error.isVisible = true;
        return;
      }
      if (this.passwordCopy.value != this.password.value) {
        this.passwordCopy.valid = false;
        this.passwordCopy.error.message = "Пароли не совпадают";
        this.passwordCopy.error.isVisible = true;
        return;
      }
      this.passwordCopy.valid = true;
      this.passwordCopy.error.message = "";
      this.passwordCopy.error.isVisible = false;
    },
  },
  computed: {
    formIsValid() {
      return (
        this.email.valid &&
        this.password.valid &&
        this.username.valid &&
        this.passwordCopy.valid
      );
    },
  },

  watch: {
    password: {
      deep: true,
      handler() {
        if (this.passwordCopy.value != "") {
          this.onPasswordCopyInput();
        }
      },
    },
  },
};
</script>

<style scoped>
.register {
  padding: 50px;
  display: flex;
  flex-direction: column;
}

.register h1 {
  text-align: center;
}

.register form {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.register .main-error {
  width: 100%;
  text-align: center;
  color: #fff;
  padding: 15px 15px;
  background-color: rgb(255 0 0 / 80%);
  display: none;
}

.register .main-error.active {
  display: block;
}

.register form .form-group {
  width: 100%;
  margin-top: 15px;
}

.register form .form-group .error {
  font-size: 14px;
  color: red;
  display: none;
}

.register form .form-group .error.active {
  display: block;
}

.register form .form-group input {
  margin-top: 5px;
}

.register form button {
  margin-top: 15px;
  width: 100%;
}

.register form button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.register .additional {
  display: flex;
  margin-top: 30px;
  justify-content: center;
}

.register .additional a {
  color: #006eaf;
  margin-left: 5px;
}
</style>
