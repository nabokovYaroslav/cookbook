import { HTTP, HTTP_AUTH } from "./common";

export const User = {
  async token(email, password) {
    const response = await HTTP.post("authentication/token/", {
      email: email,
      password: password,
    });
    return response;
  },
  async refresh() {
    const response = await HTTP.post("authentication/token/refresh/");
    return response;
  },
  async detail(username) {
    const response = await HTTP.get(`users/${username}/`);
    return response;
  },
  async authDetail(username) {
    const response = await HTTP_AUTH.get(`users/${username}/`);
    return response;
  },
  async create(email, username, password) {
    const response = await HTTP.post("users/", {
      email: email,
      user_name: username,
      password: password,
    });
    return response;
  },
  async logout() {
    const response = await HTTP.post("users/logout/");
    return response;
  },
};
