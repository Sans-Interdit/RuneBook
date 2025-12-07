import { api } from "./client";

export async function addMsg(id_conv: number, message: string, role: string) {
  try {
    const res = await api.post(`/add-msg`, { id_conv, message, role });
    return res;
  } catch (err) {
    console.error(err);
    return null;
  }
}