// src/api/client.js
import axios from "axios";

const base = import.meta.env.VITE_IP_BACK
  ? import.meta.env.VITE_IP_BACK + "/api"
  : "/api";

export const api = axios.create({
  baseURL: base,
  withCredentials: true, // utile si tu gères des cookies ou sessions
});

// Intercepteur pour log ou refresh de token
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      console.warn("Non autorisé - token invalide ou expiré");
      // éventuellement : rediriger ou rafraîchir le token
    }
    return Promise.reject(error);
  }
);
