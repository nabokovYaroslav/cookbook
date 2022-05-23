<template>
  <div>
    <div class="loader" v-if="recipesIsLoading">
      <my-spinner :size="50" />
    </div>
    <div class="row recipes" v-if="!recipesIsLoading && recipes.length !== 0">
      <div :class="wrapperClass" v-for="recipe in recipes" :key="recipe.id">
        <recipe-item
          :recipe="recipe"
          style="margin-bottom: 0; margin-top: 48px"
        />
        <div class="buttons" v-if="isOwner">
          <router-link
            :to="{
              name: 'userEditRecipe',
              params: { username: user.user_name, recipeId: recipe.id },
            }"
            class="change"
          >
            Изменить
          </router-link>
          <my-button
            @click.native="
              recipeIdToDelete = recipe.id;
              isShowDeleteRecipeForm = true;
            "
            >Удалить</my-button
          >
        </div>
      </div>
    </div>
    <div class="recipes-empty" v-if="!recipesIsLoading && recipes.length === 0">
      Пока нет рецептов
    </div>
    <my-dialog
      :show="isShowDeleteRecipeForm"
      :lock="isLockDeleteRecipeForm"
      @hide="closeDeleteRecipeForm"
    >
      <delete-recipe-form
        :recipeId="recipeIdToDelete"
        @delete="onRecipeDeleted"
        @close="closeDeleteRecipeForm"
        @formSubmitting="onFormSubmitting"
      />
    </my-dialog>
  </div>
</template>

<script>
import MyButton from "@/components/UI/MyButton";
import MySpinner from "@/components/MySpinner";
import MyDialog from "@/components/UI/MyDialog";
import DeleteRecipeForm from "@/components/DeleteRecipeForm";
import { RecipeUser } from "@/api/recipeUser";
import RecipeItem from "@/components/RecipeItem";
export default {
  components: {
    RecipeItem,
    MyButton,
    MySpinner,
    MyDialog,
    DeleteRecipeForm,
  },
  props: {
    wrapperClass: {
      type: String,
      default: "col-12 col-sm-6 col-lg-4",
    },
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
      recipes: null,
      recipesIsLoading: false,
      isShowDeleteRecipeForm: false,
      recipeIdToDelete: null,
      isLockDeleteRecipeForm: false,
    };
  },
  async created() {
    try {
      this.recipesIsLoading = true;
      const response = await RecipeUser.list(this.$route.params.username);
      this.recipes = response.data.results;
    } catch (error) {
      console.log(error);
    } finally {
      this.recipesIsLoading = false;
    }
  },
  methods: {
    closeDeleteRecipeForm() {
      this.recipeIdToDelete = null;
      this.isShowDeleteRecipeForm = false;
    },
    onRecipeDeleted(recipeId) {
      const index = this.recipes
        .map((recipe) => {
          return recipe.id;
        })
        .indexOf(recipeId);
      this.recipes.splice(index, 1);
      this.closeDeleteRecipeForm();
    },
    onFormSubmitting(lock) {
      this.isLockDeleteRecipeForm = lock;
    },
  },
};
</script>

<style scoped>
.loader {
  display: flex;
  justify-content: center;
  padding: 50px 0;
}

.recipes {
  margin-top: -48px;
}

.recipes .buttons {
  display: flex;
  justify-content: flex-end;
  margin-left: -10px;
  margin-top: 10px;
}

.recipes .buttons > * {
  margin-left: 10px;
}

.recipes .buttons .change {
  background: #ff4e00;
  display: inline-block;
  font-weight: 400;
  text-align: center;
  border: 2px solid #ff4e00;
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  line-height: 1.5;
  color: #fff;
  cursor: pointer;
  transition: 0.3s;
}

.recipes .buttons .change:hover {
  color: #ff4e00;
  background-color: #fff;
}

.recipes-empty {
  padding: 50px 0;
  text-align: center;
  font-size: 20px;
}
</style>
