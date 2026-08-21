import React, { useState } from "react";
import {
  Mail,
  Lock,
  CheckCircle,
  AlertCircle,
  Eye,
  EyeOff,
  LogIn,
} from "lucide-react";
import { useAppContext } from "../context/appContext";
import { Link, useNavigate } from "react-router-dom";

export default function Login() {
  const { loginContext } = useAppContext();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    rememberMe: false,
  });
  const navigate = useNavigate();
  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: "" }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validation
    const newErrors = {};

    if (!formData.email) {
      newErrors.email = "L'email est requis";
    } else if (!validateEmail(formData.email)) {
      newErrors.email = "Format d'email invalide";
    }

    if (!formData.password) {
      newErrors.password = "Le mot de passe est requis";
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsSubmitting(true);

    try {
      await loginContext(formData.email, formData.password);

      navigate("/profile");
    } catch (error) {
      if (error.message === "INVALID_CREDENTIALS") {
        setErrors({ submit: "Email ou mot de passe incorrect" });
      } else {
        setErrors({ submit: "Erreur serveur\nVeuillez réessayer plus tard" });
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  if (submitSuccess) {
    return (
      <div className="flex flex-col items-center justify-center overflow-auto bg-primary-50">
        <div className="max-w-md p-8 text-center border-2 rounded-2xl bg-primary-50 border-secondary-50/30">
          <div className="flex items-center justify-center w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br from-green-400 to-secondary-50">
            <CheckCircle className="w-10 h-10 text-primary-50" />
          </div>
          <h2 className="mb-4 text-3xl font-bold text-secondary-50 font-titre">
            Connexion Réussie !
          </h2>
          <p className="mb-6 text-white font-text">
            Bon retour sur RuneBook ! Redirection en cours...
          </p>
          <div className="flex justify-center">
            <div className="w-12 h-12 border-4 rounded-full border-secondary-50 border-t-transparent animate-spin"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-start justify-center flex-1 px-6 py-20 overflow-auto bg-primary-50">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="flex items-center justify-center w-16 h-16 mx-auto mb-4 rounded-full bg-primary-100">
            <LogIn className="w-8 h-8 text-primary-50" />
          </div>
          <h1 className="mb-2 text-4xl font-bold text-secondary-50 font-titre">
            Bon Retour !
          </h1>
          <p className="text-white font-text">
            Connecte-toi pour continuer ton apprentissage
          </p>
        </div>

        {/* Form */}
        <div className="p-8 border-2 rounded-2xl bg-primary-50 border-primary-100/30">
          {/* Email Field */}
          <div className="mb-6">
            <label
              htmlFor="email"
              className="block mb-2 text-sm font-semibold text-secondary-50 font-text"
            >
              Adresse Email
            </label>
            <div className="relative">
              <Mail className="absolute w-5 h-5 text-white transform -translate-y-1/2 left-4 top-1/2" />
              <input
                type="email"
                id="email"
                name="email"
                autoComplete="email"
                value={formData.email}
                onChange={handleInputChange}
                maxLength={200}
                placeholder="ton.email@example.com"
                className={`w-full py-3 pl-12 pr-4 text-white transition-all duration-300 border-2 rounded-lg bg-primary-50 placeholder-white/50 focus:outline-none font-text ${
                  errors.email
                    ? "border-red-400 focus:border-red-400"
                    : "border-primary-100/30 focus:border-secondary-50"
                }`}
              />
            </div>
            {errors.email && (
              <div className="flex items-center gap-1 mt-2 text-sm text-red-400">
                <AlertCircle className="w-4 h-4" />
                {errors.email}
              </div>
            )}
          </div>

          {/* Password Field */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <label
                htmlFor="password"
                className="text-sm font-semibold text-secondary-50 font-text"
              >
                Mot de Passe
              </label>
              {/* <Link
                to="/forgot-password" 
                className="text-xs font-semibold transition-colors text-secondary-50 hover:text-primary-100"
              >
                Mot de passe oublié ?
              </Link> */}
            </div>
            <div className="relative">
              <Lock className="absolute w-5 h-5 text-white transform -translate-y-1/2 left-4 top-1/2" />
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                name="password"
                autoComplete="current-password"
                value={formData.password}
                onChange={handleInputChange}
                maxLength={200}
                placeholder="Entre ton mot de passe"
                className={`w-full py-3 pl-12 pr-12 text-white transition-all duration-300 border-2 rounded-lg bg-primary-50 placeholder-white/50 focus:outline-none font-text ${
                  errors.password
                    ? "border-red-400 focus:border-red-400"
                    : "border-primary-100/30 focus:border-secondary-50"
                }`}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute text-white transform -translate-y-1/2 right-4 top-1/2 hover:text-secondary-50"
              >
                {showPassword ? (
                  <Eye className="w-5 h-5" />
                ) : (
                  <EyeOff className="w-5 h-5" />
                )}
              </button>
            </div>
            {errors.password && (
              <div className="flex items-center gap-1 mt-2 text-sm text-red-400">
                <AlertCircle className="w-4 h-4" />
                {errors.password}
              </div>
            )}
          </div>

          {/* Submit Error */}
          {errors.submit && (
            <div className="p-4 mb-6 border-2 rounded-lg bg-red-400/10 border-red-400/30">
              <div className="flex items-center gap-2 text-sm text-red-400">
                <AlertCircle className="w-5 h-5" />
                {errors.submit}
              </div>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="button"
            onClick={handleSubmit}
            disabled={isSubmitting}
            className="w-full py-4 text-2xl font-bold text-black transition-all duration-300 rounded-lg bg-secondary-50 hover:scale-105 hover:shadow-xl hover:shadow-secondary-50/30 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 font-titre"
          >
            {isSubmitting ? (
              <div className="flex items-center justify-center gap-2">
                <div className="w-5 h-5 border-2 rounded-full border-primary-50 border-t-transparent animate-spin"></div>
                Connexion en cours...
              </div>
            ) : (
              "Se Connecter"
            )}
          </button>

          {/* Register Link */}
          <div className="mt-6 text-center">
            <p className="text-sm text-white font-text">
              Pas encore de compte ?{" "}
              <Link
                to="/inscription"
                className="font-semibold transition-colors text-secondary-50 hover:text-primary-100"
              >
                Inscris-toi gratuitement
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
