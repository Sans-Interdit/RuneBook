import React from "react";
import { useAppContext } from "../context/appContext";

export default function Home() {
  const { message, user, login, logout } = useAppContext();

  return (
    <div className="flex flex-col items-center justify-center flex-1 text-center bg-gradient-to-br from-background-50 to-background-100 text-primary-100">
      <h1 className="mb-4 text-3xl font-bold">RuneBook</h1>
      <div className="mb-4 alert alert-info">
        {message || "Loading message from backend..."}
      </div>
      {user ? (
        <>
          <p className="mb-2">Welcome {user.name}</p>
          <button onClick={logout} className="btn">Logout</button>
        </>
      ) : (
        <button onClick={() => login("Rigo")} className="btn">Login</button>
      )}
    </div>
  );
}
