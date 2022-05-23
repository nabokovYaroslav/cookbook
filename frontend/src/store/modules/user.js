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
    isSubscribing: false,
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
    isSubscribing(state) {
      return state.isSubscribing;
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
    setUserIsSubscriber(state, isSubscriber) {
      state.user.is_subscriber = isSubscriber;
    },
    setIsSubscribing(state, isSubscribing) {
      state.isSubscribing = isSubscribing;
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

    async subscribe({ commit, getters }) {
      try {
        commit("setIsSubscribing", true);
        await User.subscribe(getters.user.user_name);
        commit("setUserIsSubscriber", true);
      } catch (error) {
        if (error.response) {
          const response = error.response;
          const status = response.status;
          if (status == 400) {
            commit("setUserIsSubscriber", true);
          } else if (status == 401) {
            await this.logout();
          }
        }
      } finally {
        commit("setIsSubscribing", false);
      }
    },

    async unsubscribe({ commit, getters }) {
      try {
        commit("setIsSubscribing", true);
        await User.unsubscribe(getters.user.user_name);
        commit("setUserIsSubscriber", false);
      } catch (error) {
        if (error.response) {
          const response = error.response;
          const status = response.status;
          if (status == 404) {
            commit("setUserIsSubscriber", false);
          } else if (status == 401) {
            await this.logout();
          }
        }
      } finally {
        commit("setIsSubscribing", false);
      }
    },
  },
};
