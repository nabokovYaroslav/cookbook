import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "@/views/HomeView";
import CategoryView from "@/views/CategoryView";
import RecipeView from "@/views/RecipeView";
import LoginView from "@/views/LoginView";
import RegisterView from "@/views/RegisterView";
import ProfileView from "@/views/ProfileView";
import UserRecipesView from "@/views/UserRecipesView";
import UserProfileView from "@/views/UserProfileView";
import UserAddRecipeView from "@/views/UserAddRecipeView";
import UserEditRecipeView from "@/views/UserEditRecipeView";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView,
  },
  {
    path: "/categories/:id",
    name: "category",
    component: CategoryView,
  },
  {
    path: "/categories/:category_id/recipes/:id",
    name: "recipe",
    component: RecipeView,
  },
  {
    path: "/:username",
    component: ProfileView,
    children: [
      {
        path: "",
        name: "profile",
        component: UserProfileView,
      },
      {
        path: "recipes",
        name: "userRecipes",
        component: UserRecipesView,
      },
      {
        path: "recipes/add",
        name: "userAddRecipe",
        component: UserAddRecipeView,
      },
      {
        path: "recipes/:recipeId/edit",
        name: "userEditRecipe",
        component: UserEditRecipeView,
      },
    ],
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
