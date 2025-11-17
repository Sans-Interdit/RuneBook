import React from "react";
import { useAppContext } from "../context/appContext";

export default function Connexion() {
  const { message, user, login, logout } = useAppContext();

  return (
    <div className="flex flex-col items-center justify-center flex-1 text-center bg-gradient-to-br from-background-50 to-background-100 text-primary-100">
      <h1 className="mb-4 text-3xl font-bold">Connexion</h1>
    </div>
  );
}
