import { api } from "./client";

export async function chat(prompt : string, character : string) {
  const res = await api.post("/chat", {prompt, character});
  return res?.data?.response;
}