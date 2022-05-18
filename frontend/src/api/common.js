import axios from "axios";
import isWebpSupport from "@/utils/supports-webp";
import { User } from "./user";

const BASE_URL = "http://localhost:8000/api/v1/";

const HTTP = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
});

HTTP.interceptors.request.use(
  async (config) => {
    const webpSupported = await isWebpSupport;
    if (webpSupported) {
      const accept = config.headers.common["Accept"].split(",");
      accept.push("image/webp");

      config.headers.common["Accept"] = accept.join(",");
    }
    return config;
  },
  (error) => {
    Promise.reject(error);
  }
);

const HTTP_AUTH = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
});

HTTP_AUTH.interceptors.request.use(
  async (config) => {
    config.headers["Authorization"] = `Bearer ${localStorage.getItem(
      "access_token"
    )}`;
    const webpSupported = await isWebpSupport;
    if (webpSupported) {
      const accept = config.headers.common["Accept"].split(",");
      accept.push("image/webp");

      config.headers.common["Accept"] = accept.join(",");
    }
    return config;
  },
  (error) => {
    Promise.reject(error);
  }
);

HTTP_AUTH.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const tokens = await User.refresh();
        localStorage.setItem("access_token", tokens.data.access);
      } catch (error) {
        return Promise.reject(error);
      }
      return HTTP_AUTH(originalRequest);
    }
    return Promise.reject(error);
  }
);

export { HTTP_AUTH, HTTP };
