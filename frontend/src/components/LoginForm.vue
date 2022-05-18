<template>
  <div class="login">
    <h1>Войти</h1>
    <form @submit.prevent="onFormSubmit">
      <div class="main-error" :class="{ active: error.isVisible }">
        {{ error.message }}
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
      <my-spinner v-if="formSubmitting" style="margin-top: 15px" :size="40" />
      <my-button v-else :disabled="!formIsValid">Войти</my-button>
    </form>
    <div class="additional">
      <p>Ещё нет аккаунта?</p>
      <router-link :to="{ name: 'register' }">Зарегистрируйтесь!</router-link>
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
      formSubmitting: false,
      error: {
        isVisible: false,
        message: "",
      },
    };
  },
  methods: {
    ...mapActions("user", {
      login: "login",
      loadUser: "loadUser",
    }),

    async onFormSubmit() {
      try {
        this.formSubmitting = true;
        await this.login({
          email: this.email.value,
          password: this.password.value,
        });
        this.loadUser();
        this.$router.push({ name: "home" });
      } catch (error) {
        if (error.response) {
          const response = error.response;
          const status = response.status;
          if (status === 401) {
            this.error.message = response.data.detail;
            this.error.isVisible = true;
          } else if (status === 400) {
            if (response.data.email) {
              (this.email.valid = false),
                (this.email.error.message = response.data.email.join("\n"));
              this.email.error.isVisible = true;
            }
            if (response.data.password) {
              (this.password.valid = false),
                (this.password.error.message = response.data.email.join("\n"));
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
  },
  computed: {
    formIsValid() {
      return this.email.valid && this.password.valid;
    },
  },
};
</script>

<style scoped>
.login {
  padding: 50px;
  display: flex;
  flex-direction: column;
}

.login h1 {
  text-align: center;
}

.login form {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login .main-error {
  width: 100%;
  text-align: center;
  color: #fff;
  padding: 15px 15px;
  background-color: rgb(255 0 0 / 80%);
  display: none;
}

.login .main-error.active {
  display: block;
}

.login form .form-group {
  width: 100%;
  margin-top: 15px;
}

.login form .form-group .error {
  font-size: 14px;
  color: red;
  display: none;
}

.login form .form-group .error.active {
  display: block;
}

.login form .form-group input {
  margin-top: 5px;
}

.login form button {
  margin-top: 15px;
  width: 100%;
}

.login form button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.login .additional {
  display: flex;
  margin-top: 30px;
  justify-content: center;
}

.login .additional a {
  color: #006eaf;
  margin-left: 5px;
}
</style>
