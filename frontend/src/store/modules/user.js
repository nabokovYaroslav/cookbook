import { User } from "@/api/user";

function hasAccessToken() {
  return localStorage.getItem("access_token") !== null ? true : false;
}

function usernameFromToken() {
  const access_token = localStorage.getItem("access_token").split(".");
  if (access_token.length !== 3) return undefined;
  const payload = access_token[1];
  const username = JSON.parse(atob(payload)).user_name;
  return username;
}

export default {
  namespaced: true,
  state: {
    user: null,
    userIsLoading: false,
  },
  getters: {
    userIsLoading(state) {
      return state.userIsLoading;
    },
    authenticated(state) {
      return state.user !== null ? true : false;
    },
    user(state) {
      return state.user;
    },
    hasAccessToken() {
      return hasAccessToken;
    },
    usernameFromToken() {
      return usernameFromToken;
    },
  },
  mutations: {
    setUserIsLoading(state, isLoading) {
      state.userIsLoading = isLoading;
    },
    setUser(state, user) {
      state.user = user;
    },
  },
  actions: {
    async loadUser({ commit }) {
      if (hasAccessToken()) {
        const username = usernameFromToken();
        if (username === undefined) throw new Error();
        try {
          commit("setUserIsLoading", true);
          const response = await User.authDetail(username);
          commit("setUser", response.data);
        } catch (error) {
          commit("setUser", null);
          await this.logout();
          throw error;
        } finally {
          commit("setUserIsLoading", false);
        }
      }
    },

    async login(store, { email, password }) {
      const response = await User.token(email, password);
      localStorage.setItem("access_token", response.data.access);
    },

    async register(store, { email, username, password }) {
      const response = await User.create(email, username, password);
      localStorage.setItem("access_token", response.data.access);
    },

    async logout({ commit }) {
      await User.logout();
      localStorage.removeItem("access_token");
      commit("setUser", null);
    },
  },
};
