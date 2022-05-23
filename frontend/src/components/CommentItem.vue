<template>
  <div class="comment-wrapper">
    <div class="comment" :id="comment.id">
      <div class="left">
        <router-link
          :to="{
            name: 'profile',
            params: { username: comment.user.user_name },
          }"
        >
          <img :src="comment.user.image" alt="user image" />
        </router-link>
      </div>
      <div class="right">
        <div class="header">
          <router-link
            class="username"
            :to="{
              name: 'profile',
              params: { username: comment.user.user_name },
            }"
          >
            {{ comment.user.user_name }}
          </router-link>
          <p class="datetime">{{ comment.datetime | normalizeDate }}</p>
        </div>
        <div class="body">
          <p class="text">{{ comment.text }}</p>
          <button class="reply" @click="onReplyClick">Ответить</button>
        </div>
      </div>
    </div>
    <div class="answers">
      <answer-comment-item
        v-for="answer in comment.answers"
        :key="answer.id"
        :answer="answer"
        :username="comment.user.user_name"
        @reply="onReply"
      />
    </div>
    <div class="answer-form" ref="answerForm">
      <answer-form
        :recipeId="comment.recipe"
        :replyTo="replyObject"
        @answerCreated="onAnswerCreated"
        v-if="replyObject !== undefined"
      />
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import AnswerCommentItem from "@/components/AnswerCommentItem";
import AnswerForm from "@/components/AnswerForm";
export default {
  components: {
    AnswerCommentItem,
    AnswerForm,
  },
  data() {
    return {
      replyObject: undefined,
    };
  },
  props: {
    comment: {
      type: Object,
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
    onReplyClick() {
      if (this.userIsLoading) return;
      if (!this.authenticated) this.$router.push({ name: "login" });
      this.replyObject = this.comment;
      this.$refs.answerForm.scrollIntoView();
    },
    onReply(replyObject) {
      if (this.userIsLoading) return;
      if (!this.authenticated) this.$router.push({ name: "login" });
      this.replyObject = replyObject;
      this.$refs.answerForm.scrollIntoView();
    },
    onAnswerCreated(answer) {
      this.$emit("answerCreated", {
        answer: answer,
        commentId: this.comment.id,
      });
      this.replyObject = undefined;
    },
  },
  computed: {
    ...mapGetters("user", {
      authenticated: "authenticated",
      userIsLoading: "userIsLoading",
    }),
  },
};
</script>

<style scoped>
.comment {
  display: flex;
  transition: 0.6s;
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

.comment-wrapper {
  margin-top: 15px;
}

.comment-wrapper .answers {
  margin-left: 65px;
}
</style>
