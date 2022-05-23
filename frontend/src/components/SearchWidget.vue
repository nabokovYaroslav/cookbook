<template>
  <div v-click-outside="closeWidget" class="search-widget">
    <search-form
      :search="search"
      @searchChange="search = $event"
      @formSubmit="onFormSubmit"
    />
    <div class="recipes" v-if="isWidgetVisible && isActive">
      <template v-if="!recipesIsLoading && recipes.length !== 0">
        <router-link
          class="recipe"
          v-for="recipe in recipes"
          :key="recipe.id"
          :to="{
            name: 'recipe',
            params: { category_id: recipe.category, id: recipe.id },
          }"
          @click.native="search = ''"
        >
          <div class="left">
            <img :src="recipe.image" alt="recipe image" />
          </div>
          <div class="right-wrapper">
            <div class="right">
              <router-link
                class="name"
                :to="{
                  name: 'recipe',
                  params: { category_id: recipe.category, id: recipe.id },
                }"
                >{{ recipe.name }}
              </router-link>
              <router-link
                class="category"
                :to="{ name: 'category', params: { id: recipe.category } }"
              >
                {{ recipe.category_name }}
              </router-link>
            </div>
          </div>
        </router-link>
      </template>
      <div class="not-found" v-if="!recipesIsLoading && recipes.length === 0">
        По вашему запросу ничего не найдено
      </div>
      <div class="loader" v-if="recipesIsLoading">
        <my-spinner :size="30" />
      </div>
    </div>
  </div>
</template>

<script>
import SearchForm from "@/components/SearchForm";
import MySpinner from "@/components/MySpinner";
import { Recipe } from "@/api/recipe";

export default {
  components: {
    SearchForm,
    MySpinner,
  },
  data() {
    return {
      search: "",
      timeout: null,
      recipes: [],
      recipesIsLoading: false,
      controller: null,
      isActive: false,
    };
  },
  computed: {
    isWidgetVisible() {
      return this.search !== "";
    },
  },
  methods: {
    loadRecipes() {
      this.controller = new AbortController();
      this.recipesIsLoading = true;
      Recipe.search_widget(this.search, this.controller.signal)
        .then((response) => {
          this.recipes = response.data.results;
          this.recipesIsLoading = false;
        })
        .catch(() => {
          this.recipesIsLoading = false;
        });
    },
    onFormSubmit() {
      if (this.search !== this.$route.query.name) {
        this.$router.push({ name: "search", query: { name: this.search } });
      }
      this.search = "";
    },
    closeWidget() {
      this.isActive = false;
    },
  },
  watch: {
    search() {
      if (this.controller !== null) {
        this.controller.abort();
        this.controller = null;
      }
      clearTimeout(this.timeout);
      if (this.search !== "") {
        this.isActive = true;
        this.recipesIsLoading = true;
        this.timeout = setTimeout(this.loadRecipes, 1000);
      } else {
        this.isActive = false;
      }
    },
  },
};
</script>

<style scoped>
.search-widget {
  display: flex;
  flex-direction: column;
  position: relative;
}

.search-widget .recipes {
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 100%;
  z-index: 2;
  left: 0;
  right: 0;
}

.search-widget .recipes > * {
  width: 100%;
}

.search-widget .recipes .recipe {
  display: flex;
  background-color: #fff;
  transition: 0.3s;
}

.search-widget .recipes .recipe:hover {
  background-color: #fff0f0;
}

.search-widget .recipes .recipe .left img {
  width: 70px;
  height: 70px;
  display: block;
}
.search-widget .recipes .recipe .right-wrapper {
  width: 100%;
  border-bottom: 1px dashed grey;
}

.search-widget .recipes .recipe .right {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  margin-left: 15px;
  height: 100%;
}

.search-widget .recipes .recipe .right .name {
  font-size: 17px;
  line-height: 1.3;
  font-weight: 700;
}

.search-widget .recipes .recipe .right .category {
  margin-top: 5px;
  padding: 0.3em 1.4em;
  background: #ff4e00;
  color: #fff;
  border-radius: 3px;
  text-decoration: none;
  font-size: 0.7em;
  transition: 0.3s;
}

.search-widget .recipes .recipe .right .category:hover {
  background: #222;
}

.search-widget .recipes .not-found {
  padding: 15px 0;
  text-align: center;
  font-size: 20px;
  background: #fff;
}

.search-widget .recipes .loader {
  padding: 15px 0;
  background: #fff;
  display: flex;
  justify-content: center;
}
</style>
