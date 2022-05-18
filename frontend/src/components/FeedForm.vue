<template>
  <div class="box">
    <form>
      <div class="caption">Получай лучшие статьи на почту каждую неделю</div>
      <div class="form">
        <my-button type="submit">Подписаться</my-button>
      </div>
    </form>
  </div>
</template>

<script>
import MyButton from "@/components/UI/MyButton";
export default {
  components: {
    MyButton,
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
  text-align: center;
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
