import { api } from "./client";

export async function getGuides() {
  const res = await api.get("/get-guides");
  return res;
}