// src/api/client.js
import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:5000/api",
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
