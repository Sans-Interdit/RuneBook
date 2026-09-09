import axios from "axios";

const base = import.meta.env.VITE_IP_BACK
  ? import.meta.env.VITE_IP_BACK + "/api"
  : "/api";

export const api = axios.create({
  baseURL: base,
  withCredentials: true,
});

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      console.warn("Non autorisé - token invalide ou expiré");
    }
    return Promise.reject(error);
  }
);
