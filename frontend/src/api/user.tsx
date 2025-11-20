import { api } from "./client";

export async function login(email, password) {
  console.log(password)
  const res = await api.post("/login", {
    email: email,
    password: password
  });
  return res;
}

export async function register(email, password) {
  const res = await api.post("/register", {
    email: email,
    password: password
  });
  return res;
}