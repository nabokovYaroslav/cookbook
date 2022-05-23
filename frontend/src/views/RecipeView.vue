<template>
  <main v-if="recipe">
    <div class="container content">
      <div class="recipe-image">
        <img
          :src="recipe.image.url"
          :srcset="recipe.image.srcset"
          sizes="(max-width: 576px) 540px,
                           (max-width: 768px) 720px,
                           (max-width: 992px) 960px,
                           1140px
                           "
          alt="recipe"
        />
        <div class="meta">
          <div class="meta-wrapper">
            <div class="category">
              <router-link
                :to="{ name: 'category', params: { id: recipe.category } }"
                >{{ recipe.category_name }}</router-link
              >
            </div>
            <span class="time">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-clock"
                viewBox="0 0 16 16"
              >
                <path
                  d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"
                />
                <path
                  d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"
                />
              </svg>
              <span>{{ recipe.time }} мин.</span>
            </span>
            <span class="date">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-calendar"
                viewBox="0 0 16 16"
              >
                <path
                  d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"
                />
              </svg>
              <span>{{ recipe.created_at }}</span>
            </span>
            <span class="comments">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-chat"
                viewBox="0 0 16 16"
              >
                <path
                  d="M2.678 11.894a1 1 0 0 1 .287.801 10.97 10.97 0 0 1-.398 2c1.395-.323 2.247-.697 2.634-.893a1 1 0 0 1 .71-.074A8.06 8.06 0 0 0 8 14c3.996 0 7-2.807 7-6 0-3.192-3.004-6-7-6S1 4.808 1 8c0 1.468.617 2.83 1.678 3.894zm-.493 3.905a21.682 21.682 0 0 1-.713.129c-.2.032-.352-.176-.273-.362a9.68 9.68 0 0 0 .244-.637l.003-.01c.248-.72.45-1.548.524-2.319C.743 11.37 0 9.76 0 8c0-3.866 3.582-7 8-7s8 3.134 8 7-3.582 7-8 7a9.06 9.06 0 0 1-2.347-.306c-.52.263-1.639.742-3.468 1.105z"
                />
              </svg>
              <span>{{ recipe.comments_count }}</span>
            </span>
            <span class="views">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-eye"
                viewBox="0 0 16 16"
              >
                <path
                  d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"
                />
                <path
                  d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"
                />
              </svg>
              <span>{{ recipe.views_count }}</span>
            </span>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-12 col-lg-8">
          <div class="recipe-content">
            <h1 class="recipe-title">{{ recipe.name }}</h1>
            <p class="recipe-description">
              {{ recipe.description }}
            </p>
            <div class="ingredients-block">
              <ingredient-list
                :ingredients="recipe.ingredients"
                :serves="recipe.count"
              />
              <div class="nutritional">
                <div class="nutritional-header">На порцию</div>
                <div class="nutritional-group">
                  <span>Калории</span>
                  <span>{{ recipe.colorie }} <strong>калл</strong></span>
                </div>
                <div class="nutritional-group">
                  <span>Белки</span>
                  <span>{{ recipe.protein }} <strong>г</strong></span>
                </div>
                <div class="nutritional-group">
                  <span>Жиры</span>
                  <span>{{ recipe.fat }} <strong>г</strong></span>
                </div>
                <div class="nutritional-group">
                  <span>Углеводы</span>
                  <span>{{ recipe.carbohydrate }} <strong>г</strong></span>
                </div>
              </div>
            </div>
            <div class="steps-wrapper">
              <div class="steps-header">Шаги</div>
              <ul class="steps">
                <li v-for="step in recipe.steps" :key="step.id">
                  <div class="image">
                    <img
                      :src="step.image.url"
                      :srcset="step.image.srcset"
                      sizes="(max-width: 576px) 540px,
                           (max-width: 768px) 720px,
                           (max-width: 992px) 960px,
                           1140px
                           "
                      alt=""
                    />
                  </div>
                  <div class="text">
                    {{ step.description }}
                  </div>
                </li>
              </ul>
            </div>
            <hr />
            <p class="result">
              {{ recipe.result }}
            </p>
          </div>
          <h2>Комментарии</h2>
          <comment-list :recipeId="recipe.id" class="comments" />
        </div>
        <div class="col-12 col-lg-4 additional">
          <popular-recipe-widget-list />
          <feed-form />
          <week-recipe-widget-list />
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import PopularRecipeWidgetList from "@/components/PopularRecipeWidgetList";
import WeekRecipeWidgetList from "@/components/WeekRecipeWidgetList";
import FeedForm from "@/components/FeedForm";
import IngredientList from "@/components/IngredientList";
import CommentList from "@/components/CommentList";
import { Recipe } from "@/api/recipe";
import { View } from "@/api/view";

export default {
  components: {
    PopularRecipeWidgetList,
    FeedForm,
    WeekRecipeWidgetList,
    IngredientList,
    CommentList,
  },
  data() {
    return {
      recipe: null,
      recipeIsLoading: false,
      userIsLoadingUnwatch: null,
    };
  },
  computed: {
    ...mapGetters("user", {
      authenticated: "authenticated",
      userIsLoading: "userIsLoading",
      user: "user",
    }),
  },
  methods: {
    ...mapActions("user", {
      logout: "logout",
    }),
    sendView() {
      View.create(this.$route.params.id, this.user.user).catch(() => {});
    },
  },
  async created() {
    try {
      this.recipeIsLoading = true;
      const response = await Recipe.detail(this.$route.params.id);
      this.recipe = response.data;
    } catch (error) {
      if (error.response) {
        const response = error.response;
        const status = response.status;
        if (status != 404) {
          throw error;
        }
      }
      throw error;
    } finally {
      this.recipeIsLoading = false;
    }
    if (this.authenticated) {
      this.sendView();
    } else {
      this.authenticatedUnwatch = this.$watch("userIsLoading", () => {
        if (this.authenticated) {
          this.sendView();
        }
        this.userIsLoadingUnwatch();
      });
    }
  },
};
</script>

<style scoped>
/* content */

.content {
  padding: 0 30px;
  box-shadow: 0 0 100px rgb(178 165 105 / 19%);
  background-color: #fff;
}

.content .comments {
  padding: 50px 0;
}

.content .recipe-image {
  margin-left: -30px;
  position: relative;
}

.content .recipe-image img {
  width: calc(100% + 30px);
  height: 400px;
  object-fit: cover;
  display: block;
}

.content .recipe-image .meta {
  position: absolute;
  width: calc(100% + 30px);
  padding: 120px 50px 20px 50px;
  bottom: 0;
  left: 0;
  color: rgba(255, 255, 255, 0.7);
  background-image: linear-gradient(to bottom, transparent, rgba(0, 0, 0, 0.2));
}

.content .recipe-image .meta .meta-wrapper {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  margin-left: -20px;
  margin-top: -10px;
}

.content .recipe-image .meta .meta-wrapper > * {
  margin-left: 20px;
  margin-top: 10px;
}

.content .recipe-image .meta .meta-wrapper .time,
.content .recipe-image .meta .meta-wrapper .date,
.content .recipe-image .meta .meta-wrapper .comments,
.content .recipe-image .meta .meta-wrapper .views {
  display: flex;
  align-items: center;
}

.content .recipe-image .meta .meta-wrapper .time > span,
.content .recipe-image .meta .meta-wrapper .date > span,
.content .recipe-image .meta .meta-wrapper .comments > span,
.content .recipe-image .meta .meta-wrapper .views > span {
  margin-left: 10px;
  font-size: 14px;
  margin-top: 3px;
}

.content .recipe-image .meta svg {
  fill: rgba(255, 255, 255, 0.7);
}

.content .recipe-image .meta .category a {
  display: inline-block;
  padding: 6px 13px;
  background: #ff4e00;
  color: #fff;
  border-radius: 3px;
  transition: all 0.3s;
  font-size: 14px;
}

.content .recipe-image .meta .category a:hover {
  background-color: #222;
}

.content > .row {
  margin-top: 30px;
}

.content .recipe-title {
  font-size: 40px;
  font-weight: 700;
}

.content .recipe-description {
  font-size: 16px;
  margin-top: 16px;
}

.content .ingredients-block {
  display: flex;
  align-items: baseline;
  margin-top: 24px;
}

.content .nutritional {
  font-size: 13px;
  padding: 15px;
  background: #f3f3f3;
  flex: 0 0 30%;
  max-width: 30%;
}

.content .nutritional .nutritional-header {
  max-width: 300px;
  margin: 0 auto 0.5rem auto;
  font-size: 1.1em;
  font-weight: 700;
  color: #ff4e00;
}

.content .nutritional .nutritional-group {
  display: flex;
  max-width: 300px;
  margin: 5px auto 5px auto;
  justify-content: space-between;
}

.content .nutritional .nutritional-group span:first-child {
  width: 100%;
  flex: 0 0 60%;
  max-width: 60%;
}

.content .nutritional .nutritional-group span:last-child {
  width: 100%;
  flex: 0 0 40%;
  max-width: 40%;
}

.content .steps-wrapper {
  margin-top: 24px;
}

.content .steps-wrapper .steps-header {
  padding-top: 3px;
  padding-left: 40px;
  font-weight: 700;
  font-size: 18px;
  background: 0 0 url(@/assets/img/steps.svg) no-repeat;
}

.content .steps-wrapper .steps {
  margin-top: 24px;
}

.content .steps-wrapper .steps {
  padding-left: 40px;
  counter-reset: step;
}

.content .steps-wrapper .steps li {
  padding: 24px 0;
  display: flex;
  align-items: center;
  position: relative;
}

.content .steps-wrapper .steps li:not(:last-child) {
  border-bottom: 1px solid #f3f3f3;
}

.content .steps-wrapper .steps li .image {
  flex: 0 0 330px;
  max-width: 330px;
  margin-right: 30px;
}

.content .steps-wrapper .steps li .image img {
  max-width: 100%;
  height: auto;
  display: block;
}

.content .steps-wrapper .steps li .text {
  font-size: 16px;
  line-height: 1.5;
}

.content .steps-wrapper .steps li::before {
  counter-increment: step;
  content: counter(step);
  position: absolute;
  left: -40px;
  top: 1.5rem;
  width: 30px;
  text-align: center;
  font-size: 22px;
  color: #666;
  opacity: 0.4;
  transition: 0.3s;
}

.content .steps-wrapper .steps li:hover::before {
  opacity: 1;
}

.content hr {
  margin-top: 16px;
  margin-bottom: 16px;
  border: 0;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.content .result {
  font-size: 16px;
  line-height: 1.5;
  margin-bottom: 24px;
}

@media (max-width: 767px) {
  .content .steps-wrapper .steps li {
    display: block;
  }

  .content .ingredients-block {
    display: block;
  }

  .content .steps-wrapper .steps li .text {
    margin-top: 15px;
  }

  .content .nutritional {
    max-width: none;
    flex: none;
    margin-top: 15px;
  }
}

.additional {
  display: none;
}

@media (min-width: 992px) {
  .additional {
    display: block;
  }
}

/* content */
</style>
