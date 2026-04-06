import { api } from "./client";

export async function getGuide(id : number) {
  const res = await api.get(`/guides/${id}`);
  return res;
}

export async function getGuides() {
  const res = await api.get("/guides");
  return res;
}