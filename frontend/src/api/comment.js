import { HTTP_AUTH } from "@/api/common";

export const Comment = {
  async create(recipeId, user, replyTo, text) {
    const response = await HTTP_AUTH.post(`comments/`, {
      user: user,
      reply_to: replyTo,
      text: text,
      recipe: recipeId,
    });
    return response;
  },
};
