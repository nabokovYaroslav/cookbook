<template>
  <div class="comment" :id="answer.id">
    <div class="left">
      <router-link
        :to="{
          name: 'profile',
          params: { username: answer.user.user_name },
        }"
      >
        <img :src="answer.user.image" alt="user image" />
      </router-link>
    </div>
    <div class="right">
      <div class="header">
        <router-link
          class="username"
          :to="{
            name: 'profile',
            params: { username: answer.user.user_name },
          }"
        >
          {{ answer.user.user_name }}
        </router-link>
        <p class="datetime">{{ answer.datetime | normalizeDate }}</p>
        <a
          @click.prevent="onSourceClick"
          :href="'#' + answer.reply_to"
          class="reply-to"
          >ответ к комментарию <b>@{{ username }}</b></a
        >
      </div>
      <div class="body">
        <p class="text">{{ answer.text }}</p>
        <button class="reply" @click="$emit('reply', answer)">Ответить</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    answer: {
      type: Object,
      required: true,
    },
    username: {
      type: String,
      required: true,
    },
  },
  filters: {
    normalizeDate(value) {
      const date = new Date(value);
      const day = date.getDay() < 10 ? "0" + date.getDay() : date.getDay();
      const month =
        date.getDay() < 10 ? "0" + date.getMonth() : date.getMonth();
      const hours =
        date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
      const minutes =
        date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
      return `${day}.${month}.${date.getFullYear()} в ${hours}:${minutes}`;
    },
  },
  methods: {
    onSourceClick() {
      const source = document.getElementById(this.answer.reply_to);
      source.scrollIntoView();
      source.addEventListener("transitionend", transitionHandler);
      source.classList.add("active");
      function transitionHandler() {
        source.classList.remove("active");
        source.removeEventListener("transitionend", transitionHandler);
      }
    },
  },
};
</script>

<style scoped>
.comment {
  display: flex;
  margin-top: 15px;
  transition: 0.3s;
}

.comment.active {
  background-color: rgb(255 0 0 / 20%);
}

.comment .left img {
  width: 50px;
  height: 50px;
  display: block;
  border-radius: 50%;
}

.comment .right {
  display: flex;
  flex-direction: column;
  margin-left: 15px;
}

.comment .right .header {
  display: flex;
  margin-left: -20px;
  align-items: center;
}

.comment .right .header > * {
  margin-left: 20px;
}

.comment .right .header .datetime {
  color: #999;
  font-size: 13px;
  opacity: 0.6;
}

.comment .right .header .username {
  font-weight: 700;
  color: #333;
}

.comment .right .body {
  margin-top: 10px;
}

.comment .right .body .text {
  font-size: 0.95em;
  line-height: 1.35;
  word-break: break-word;
}

.comment .right .body .reply {
  margin-top: 16px;
  transition: 0.3s;
  font-size: 0.85em;
  cursor: pointer;
  outline: none;
  border: none;
  background-color: transparent;
  color: #ff4e00;
  opacity: 0;
}

.comment:hover .right .body .reply {
  opacity: 1;
}

.comment .reply-to {
  color: #333;
  font-size: 14px;
}
</style>
