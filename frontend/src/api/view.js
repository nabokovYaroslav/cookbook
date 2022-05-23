import { HTTP_AUTH } from "./common";

export const View = {
  async create(recipeId, user) {
    const response = await HTTP_AUTH.post("views/", {
      recipe: recipeId,
      user: user,
    });
    return response;
  },
};
