import { CheckCircle, Trash2 } from "lucide-react";
import React, { useEffect } from "react";
import { useAppContext } from "../context/appContext";
import { useNavigate } from "react-router-dom";

export default function SupprAcc() {
  const { supprAccContext, logoutContext } = useAppContext();
  const navigate = useNavigate();

  useEffect(() => {
    supprAccContext();
    logoutContext();
    // Redirect after success
    navigate("/");
  }, []);

  return (
    <div className="flex items-center justify-center flex-1 bg-primary-50">
      <div className="max-w-md p-8 text-center border-2 rounded-2xl bg-primary-50 border-secondary-50/30">
        <div className="flex items-center justify-center w-20 h-20 mx-auto mb-6 bg-red-800 rounded-full">
          <Trash2 className="w-10 h-10 text-primary-50" />
        </div>
        <h2 className="mb-4 text-3xl font-bold text-secondary-50 font-titre">
          Suppression du compte en cours...
        </h2>
        <p className="mb-6 text-white font-text">
          Toutes vos données seront supprimés
        </p>
        <div className="flex justify-center">
          <div className="w-12 h-12 border-4 rounded-full border-secondary-50 border-t-transparent animate-spin"></div>
        </div>
      </div>
    </div>
  );
}
