import { HTTP } from "./common";

export const RecipeUser = {
  async list(username) {
    const response = await HTTP.get(`users/${username}/recipes/`);
    return response;
  },
};
