<template>
  <div class="comments">
    <comment-item
      v-for="comment in comments"
      :key="comment.id"
      :comment="comment"
      @answerCreated="onAnswerCreated"
    />
    <div class="loader" v-if="commentsIsLoading">
      <my-spinner :size="50" />
    </div>
    <div class="not-found" v-if="!commentsIsLoading && comments.length === 0">
      У этого рецепта ещё нет комментариев. Будьте первым!
    </div>
    <my-button
      v-if="next && !nextIsLoading"
      style="margin-top: 15px"
      @click.native="onNextClick"
      >Показать все комментарии</my-button
    >
    <div class="loader" v-if="nextIsLoading" style="margin-top: 15px">
      <my-spinner :size="40" />
    </div>
    <comment-form
      :recipeId="this.$route.params.id"
      v-if="!userIsLoading && authenticated"
      @commentCreated="onCommentCreated"
      style="margin-top: 15px"
    />
    <div class="not-allowed" v-if="!userIsLoading && !authenticated">
      Только авторизованные пользователи могут оставлять комментарии
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { HTTP } from "@/api/common";
import CommentItem from "@/components/CommentItem";
import CommentForm from "@/components/CommentForm";
import { CommentRecipe } from "@/api/commentRecipe";
import MySpinner from "@/components/MySpinner";
import MyButton from "@/components/UI/MyButton";

export default {
  components: {
    CommentItem,
    MySpinner,
    MyButton,
    CommentForm,
  },
  props: {
    recipeId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      comments: [],
      commentsIsLoading: false,
      next: null,
      nextIsLoading: false,
      nextPromise: null,
    };
  },
  methods: {
    getAllAnswersFromComment(comment) {
      const answers = [];
      comment.answers.forEach((answer) => {
        answers.push(answer);
        if (answer.answers.length != 0) {
          answers.push(...this.getAllAnswersFromComment(answer));
        }
      });
      return answers;
    },
    getAllComments() {
      if (this.nextIsLoading == true || this.next === null) return;
      this.nextIsLoading = true;
      const promise = HTTP.get(this.next, {
        params: {
          all: true,
        },
      })
        .then((response) => {
          this.next = null;
          this.comments.push(
            ...response.data.map((result) => {
              const comment = JSON.parse(JSON.stringify(result));
              comment.answers = this.getAllAnswersFromComment(comment);
              comment.answers.sort(this.sortByDatetime);
              return comment;
            })
          );
          this.nextIsLoading = false;
        })
        .catch(() => {
          this.nextIsLoading = false;
        });
      this.nextPromise = promise;
    },
    sortByDatetime(a, b) {
      const firstCommentCreatedAt = new Date(a.datetime);
      const secondCommentCreatedAt = new Date(b.datetime);
      if (firstCommentCreatedAt < secondCommentCreatedAt) {
        return -1;
      }
      if (firstCommentCreatedAt > secondCommentCreatedAt) {
        return 1;
      }
      return 0;
    },
    onNextClick() {
      this.getAllComments();
    },
    async onCommentCreated(comment) {
      if (this.next != null && this.nextPromise == null) {
        this.getAllComments();
        await this.nextPromise;
        document.getElementById(comment.id).scrollIntoView();
      } else if (this.next != null && this.nextPromise !== null) {
        await this.nextPromise;
        this.comments.push(comment);
        await this.$nextTick();
        document.getElementById(comment.id).scrollIntoView();
      } else {
        this.comments.push(comment);
        await this.$nextTick();
        document.getElementById(comment.id).scrollIntoView();
      }
    },
    onAnswerCreated(answer) {
      const index = this.comments
        .map((comment) => {
          return comment.id;
        })
        .indexOf(answer.commentId);
      this.comments[index].answers.push(answer.answer);
    },
  },
  created() {
    this.commentsIsLoading = true;
    CommentRecipe.list(this.$route.params.id)
      .then((response) => {
        this.comments = response.data.results.map((result) => {
          const comment = JSON.parse(JSON.stringify(result));
          comment.answers = this.getAllAnswersFromComment(comment);
          comment.answers.sort(this.sortByDatetime);
          return comment;
        });
        this.next = response.data.next;
        this.commentsIsLoading = false;
      })
      .catch(() => {
        this.commentsIsLoading = false;
      });
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
.comments {
  display: flex;
  flex-direction: column;
  margin-top: -15px;
}

.comments .loader {
  display: flex;
  justify-content: center;
}

.comments .not-found {
  font-size: 20px;
  text-align: center;
  font-weight: 600;
}

.comments .not-allowed {
  margin-top: 15px;
  text-align: center;
  font-size: 20px;
  font-weight: 600;
}
</style>
