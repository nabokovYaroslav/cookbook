import { HTTP } from "./common";

export const Category = {
  async list() {
    const response = await HTTP.get("categories/");
    return response;
  },

  async detail(category_id) {
    const response = await HTTP.get(`categories/${category_id}/`);
    return response;
  },
};
