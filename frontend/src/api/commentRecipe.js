import { HTTP } from "@/api/common";

export const CommentRecipe = {
  async list(recipeId) {
    const response = await HTTP.get(`recipes/${recipeId}/comments/`);
    return response;
  },
};
