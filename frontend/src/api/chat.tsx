import { api } from "./client";

export async function chat(prompt : string) {
  const res = await api.post("/chat", {prompt});
  return res;
}