import { HTTP } from "./common";

export const RecipeCategory = {
  async list(category_id) {
    const response = await HTTP.get(`categories/${category_id}/recipes/`);
    return response;
  },
};
