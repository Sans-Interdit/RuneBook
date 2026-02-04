import { api } from "./client";

export async function delConv(id : string) {
  try {
    const res = await api.delete(`/del-conv?id=${id}`);
    return res;
  } catch (err) {
    console.error(err);
    return null;
  }
}

export async function addConv(title: string, character: string) {
  try {
    const res = await api.post(`/add-conv`, { title, character });
    return res;
  } catch (err) {
    console.error(err);
    return null;
  }
}

export async function getConv(character: string) {
  try {
    const res = await api.get(`/get-conv?character=${character}`);
    return res;
  } catch (err) {
    console.error(err);
    return [];
  }
}