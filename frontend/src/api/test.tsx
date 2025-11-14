import { api } from "./client";

export async function test() {
  const res = await api.get("/hello");
  return res.data;
}