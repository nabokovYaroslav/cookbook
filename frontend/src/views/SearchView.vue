<template>
  <main>
    <div class="container">
      <search-form
        :search="search"
        @searchChange="search = $event"
        @formSubmit="onFormSubmit"
      />
      <div class="recipes-wrapper">
        <div class="loader" v-if="recipesIsLoading">
          <my-spinner :size="50" />
        </div>
        <div
          class="not-found"
          v-if="!recipesIsLoading && recipes.length === 0 && name !== ''"
        >
          По вашему запросу ничего не найдено
        </div>
        <div class="input-query" v-if="name == ''">Введите запрос</div>
        <recipe-list
          :recipes="recipes"
          v-if="!recipesIsLoading && recipes.length !== 0"
        />
      </div>
    </div>
  </main>
</template>

<script>
import SearchForm from "@/components/SearchForm";
import MySpinner from "@/components/MySpinner";
import RecipeList from "@/components/RecipeList";
import { Recipe } from "@/api/recipe";
export default {
  components: {
    SearchForm,
    MySpinner,
    RecipeList,
  },
  data() {
    return {
      search: "",
      recipes: [],
      recipesIsLoading: false,
      controller: null,
    };
  },
  computed: {
    name() {
      return this.$route.query.name || "";
    },
  },
  methods: {
    loadRecipes() {
      if (this.controller !== null) {
        this.controller.abort();
        this.controller = null;
      }
      this.controller = new AbortController();
      this.recipesIsLoading = true;
      Recipe.search(this.search, this.controller.signal)
        .then((response) => {
          this.recipes = response.data.results;
          this.recipesIsLoading = false;
        })
        .catch(() => {
          this.recipesIsLoading = false;
        });
    },
    onFormSubmit() {
      if (this.search !== this.name) {
        this.$router.push({ name: "search", query: { name: this.search } });
      }
    },
  },
  watch: {
    name() {
      this.search = this.name;
      this.loadRecipes();
    },
  },
  created() {
    this.search = this.name;
    if (this.search !== "") {
      this.loadRecipes();
    }
  },
};
</script>

<style scoped>
main {
  padding: 50px 0;
}
.recipes-wrapper {
  padding: 50px 0;
}

.recipes-wrapper .loader {
  display: flex;
  justify-content: center;
}

.recipes-wrapper .input-query,
.recipes-wrapper .not-found {
  text-align: center;
  font-size: 20px;
  font-weight: 600;
}
</style>
