import { title } from "process";
import { api } from "./client";

export function delConv(id : string) {
  api.delete(`/del-conv?id=${id}`)
  .then((res) => {
    return res;
  })
  .catch((err) => {
    console.error(err)
  })
}

export function addConv(title : string) {
  api.post(`/add-conv`, {
    title: title
  })
  .then((res) => {
    return res;
  })
  .catch((err) => {
    console.error(err)
  })
}