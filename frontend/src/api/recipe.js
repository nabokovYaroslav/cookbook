import { HTTP, HTTP_AUTH } from "./common";

export const Recipe = {
  async create(
    name,
    category,
    description,
    time,
    colorie,
    protein,
    fat,
    carbohydrate,
    count,
    image,
    ingredients,
    steps,
    result,
    user
  ) {
    const response = await HTTP_AUTH.post("recipes/", {
      name: name,
      category: category,
      description: description,
      time: time,
      colorie: colorie,
      protein: protein,
      fat: fat,
      carbohydrate: carbohydrate,
      count: count,
      image: image,
      ingredients: ingredients,
      steps: steps,
      result: result,
      user: user,
    });
    return response;
  },

  async detail(recipe_id) {
    const response = await HTTP.get(`recipes/${recipe_id}/`);
    return response;
  },

  async edit(recipe_id) {
    const response = await HTTP_AUTH.get(`recipes/${recipe_id}/edit/`);
    return response;
  },

  async update(
    recipe_id,
    name,
    category,
    description,
    time,
    colorie,
    protein,
    fat,
    carbohydrate,
    count,
    image,
    ingredients,
    steps,
    result,
    user
  ) {
    const response = await HTTP_AUTH.put(`recipes/${recipe_id}/`, {
      name: name,
      category: category,
      description: description,
      time: time,
      colorie: colorie,
      protein: protein,
      fat: fat,
      carbohydrate: carbohydrate,
      count: count,
      image: image,
      ingredients: ingredients,
      steps: steps,
      result: result,
      user: user,
    });
    return response;
  },

  async destroy(recipe_id) {
    const response = await HTTP_AUTH.delete(`recipes/${recipe_id}/`);
    return response;
  },

  async recipes_of_week() {
    const response = await HTTP.get("recipes/recipes_of_week/");
    return response;
  },

  async popular_recipes() {
    const response = await HTTP.get("recipes/popular_recipes/");
    return response;
  },

  async popular_recipes_widget() {
    const response = await HTTP.get("recipes/popular_recipes_widget/");
    return response;
  },

  async recipes_of_week_widget() {
    const response = await HTTP.get("recipes/recipes_of_week_widget/");
    return response;
  },

  async new_recipes() {
    const response = await HTTP.get("recipes/new_recipes/");
    return response;
  },

  async random_recipes() {
    const response = await HTTP.get("recipes/random_recipes/");
    return response;
  },

  async search_widget(name, signal) {
    const response = await HTTP.get(`recipes/search_widget?name=${name}`, {
      signal: signal,
    });
    return response;
  },

  async search(name, signal) {
    const response = await HTTP.get(`recipes/search?name=${name}`, {
      signal: signal,
    });
    return response;
  },
};
