import { CheckCircle } from "lucide-react";
import React, { useEffect } from "react";
import { useAppContext } from "../context/appContext";

export default function Logout() {
  const { logoutContext } = useAppContext();
  useEffect(()=> {
    logoutContext();

    // Redirect after success
    window.location.href = '/';
  }, [])


  return (
    <div className="flex items-center justify-center flex-1 bg-primary-50">
      <div className="max-w-md p-8 text-center border-2 rounded-2xl bg-primary-50 border-secondary-50/30">
        <div className="flex items-center justify-center w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br from-green-400 to-secondary-50">
          <CheckCircle className="w-10 h-10 text-primary-50" />
        </div>
        <h2 className="mb-4 text-3xl font-bold text-secondary-50 font-titre">
          Déconnection
        </h2>
        <p className="mb-6 text-white font-text">
          Merci d'être passé ! Redirection en cours...
        </p>
        <div className="flex justify-center">
          <div className="w-12 h-12 border-4 rounded-full border-secondary-50 border-t-transparent animate-spin"></div>
        </div>
      </div>
    </div>
  );
}
