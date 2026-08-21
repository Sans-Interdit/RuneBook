import { Cpu } from "lucide-react";
import { api } from "./client";

export async function login(email, password) {
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

export async function logout() {
  const res = await api.get("/logout");
  return res;
}

export async function suppressAcc() {
  const res = await api.delete("/suppr-acc");
  return res;
}

export async function getEmail() {
  const res = await api.get("/get-email");
  return res.data;
}

export async function getId() {
  const res = await api.get("/me");
  return res;
}

export async function changeEmail(email) {
  const res = await api.put("/change-email", {
    email: email,
  });
  return res;
}

export async function changePassword(password) {
  const res = await api.put("/change-password", {
    password: password
  });
  return res;
}
