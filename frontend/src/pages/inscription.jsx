import React, { useState } from "react";
import { Mail, Lock, CheckCircle, AlertCircle, Eye, EyeOff, UserPlus } from "lucide-react";
import { useAppContext } from "../context/appContext";

export default function Inscription() {
  const { registerContext } = useAppContext();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
    consent: false
  });

  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validatePassword = (password) => {
    return password.length >= 8;
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
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
    } else if (!validatePassword(formData.password)) {
      newErrors.password = "Le mot de passe doit contenir au moins 8 caractères";
    }
    
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = "Veuillez confirmer votre mot de passe";
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = "Les mots de passe ne correspondent pas";
    }
    
    if (!formData.consent) {
      newErrors.consent = "Vous devez accepter les conditions pour continuer";
    }
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    
    // Submit form
    setIsSubmitting(true);
    
    try {
      registerContext(formData.email, formData.password)
      
      setSubmitSuccess(true);
      
      // Redirect after success
      setTimeout(() => {
        window.location.href = '/chatbot';
      }, 2000);
      
    } catch (error) {
      setErrors({ submit: "Une erreur est survenue. Veuillez réessayer." });
    } finally {
      setIsSubmitting(false);
    }
  };

  const getPasswordStrength = (password) => {
    if (!password) return { strength: 0, label: "", color: "" };
    
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;
    
    if (strength <= 2) return { strength, label: "Faible", color: "bg-red-400" };
    if (strength <= 3) return { strength, label: "Moyen", color: "bg-secondary-50" };
    return { strength, label: "Fort", color: "bg-green-400" };
  };

  const passwordStrength = getPasswordStrength(formData.password);

  if (submitSuccess) {
    return (
      <div className="flex items-center justify-center flex-1 bg-primary-50">
        <div className="max-w-md p-8 text-center border-2 rounded-2xl bg-primary-50 border-secondary-50/30">
          <div className="flex items-center justify-center w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br from-green-400 to-secondary-50">
            <CheckCircle className="w-10 h-10 text-primary-50" />
          </div>
          <h2 className="mb-4 text-3xl font-bold text-secondary-50 font-titre">
            Inscription Réussie !
          </h2>
          <p className="mb-6 text-white font-text">
            Bienvenue sur RuneBook ! Tu vas être redirigé vers le chatbot...
          </p>
          <div className="flex justify-center">
            <div className="w-12 h-12 border-4 rounded-full border-secondary-50 border-t-transparent animate-spin"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center flex-1 px-6 bg-primary-50">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="flex items-center justify-center w-16 h-16 mx-auto mb-4 rounded-full bg-primary-100">
            <UserPlus className="w-8 h-8 text-primary-50" />
          </div>
          <h1 className="mb-2 text-4xl font-bold text-secondary-50 font-titre">
            Rejoins RuneBook
          </h1>
          <p className="text-white font-text">
            Commence ton aventure dans la comprehension de l'univers de League of Legends
          </p>
        </div>

        {/* Form */}
        <div className="p-8 border-2 rounded-2xl bg-primary-50 border-primary-100/30">
          {/* Email Field */}
          <div className="mb-6">
            <label htmlFor="email" className="block mb-2 text-sm font-semibold text-secondary-50 font-text">
              Adresse Email
            </label>
            <div className="relative">
              <Mail className="absolute w-5 h-5 text-white transform -translate-y-1/2 left-4 top-1/2" />
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder="ton.email@example.com"
                className={`w-full py-3 pl-12 pr-4 text-white transition-all duration-300 border-2 rounded-lg bg-primary-50 placeholder-white/50 focus:outline-none font-text ${
                  errors.email 
                    ? 'border-red-400 focus:border-red-400' 
                    : 'border-primary-100/30 focus:border-secondary-50'
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
            <label htmlFor="password" className="block mb-2 text-sm font-semibold text-secondary-50 font-text">
              Mot de Passe
            </label>
            <div className="relative">
              <Lock className="absolute w-5 h-5 text-white transform -translate-y-1/2 left-4 top-1/2" />
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                placeholder="Minimum 8 caractères"
                className={`w-full py-3 pl-12 pr-12 text-white transition-all duration-300 border-2 rounded-lg bg-primary-50 placeholder-white/50 focus:outline-none font-text ${
                  errors.password 
                    ? 'border-red-400 focus:border-red-400' 
                    : 'border-primary-100/30 focus:border-secondary-50'
                }`}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute text-white transform -translate-y-1/2 right-4 top-1/2 hover:text-secondary-50"
              >
                {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
            {formData.password && (
              <div className="mt-2">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs text-white">Force du mot de passe</span>
                  <span className={`text-xs font-semibold ${passwordStrength.color.replace('bg-', 'text-')}`}>
                    {passwordStrength.label}
                  </span>
                </div>
                <div className="h-2 overflow-hidden rounded-full bg-primary-100/30">
                  <div 
                    className={`h-full transition-all duration-300 ${passwordStrength.color}`}
                    style={{ width: `${(passwordStrength.strength / 5) * 100}%` }}
                  ></div>
                </div>
              </div>
            )}
            {errors.password && (
              <div className="flex items-center gap-1 mt-2 text-sm text-red-400">
                <AlertCircle className="w-4 h-4" />
                {errors.password}
              </div>
            )}
          </div>

          {/* Confirm Password Field */}
          <div className="mb-6">
            <label htmlFor="confirmPassword" className="block mb-2 text-sm font-semibold text-secondary-50 font-text">
              Confirmer le Mot de Passe
            </label>
            <div className="relative">
              <Lock className="absolute w-5 h-5 text-white transform -translate-y-1/2 left-4 top-1/2" />
              <input
                type={showConfirmPassword ? "text" : "password"}
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                placeholder="Retape ton mot de passe"
                className={`w-full py-3 pl-12 pr-12 text-white transition-all duration-300 border-2 rounded-lg bg-primary-50 placeholder-white/50 focus:outline-none font-text ${
                  errors.confirmPassword 
                    ? 'border-red-400 focus:border-red-400' 
                    : 'border-primary-100/30 focus:border-secondary-50'
                }`}
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute text-white transform -translate-y-1/2 right-4 top-1/2 hover:text-secondary-50"
              >
                {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
            {errors.confirmPassword && (
              <div className="flex items-center gap-1 mt-2 text-sm text-red-400">
                <AlertCircle className="w-4 h-4" />
                {errors.confirmPassword}
              </div>
            )}
          </div>

          {/* Consent Checkbox */}
          <div className="mb-6">
            <label className="flex items-start gap-3 cursor-pointer group">
              <div className="relative flex-shrink-0 mt-1">
                <input
                  type="checkbox"
                  name="consent"
                  checked={formData.consent}
                  onChange={handleInputChange}
                  className="w-5 h-5 transition-all duration-300 border-2 rounded appearance-none cursor-pointer bg-primary-50 border-primary-100/30 checked:bg-secondary-50 checked:border-secondary-50 focus:outline-none focus:ring-2 focus:ring-secondary-50/50"
                />
                {formData.consent && (
                  <CheckCircle className="absolute w-5 h-5 transform -translate-x-1/2 -translate-y-1/2 pointer-events-none text-primary-50 top-1/2 left-1/2" />
                )}
              </div>
              <span className="text-sm text-white font-text">
                J'accepte les{" "}
                <a href="/terms" className="font-semibold underline text-secondary-50 hover:text-primary-100">
                  conditions d'utilisation
                </a>{" "}
                et la{" "}
                <a href="/privacy" className="font-semibold underline text-secondary-50 hover:text-primary-100">
                  politique de confidentialité
                </a>{" "}
                de RuneBook. Je consens au traitement de mes données personnelles conformément à ces politiques.
              </span>
            </label>
            {errors.consent && (
              <div className="flex items-center gap-1 mt-2 text-sm text-red-400">
                <AlertCircle className="w-4 h-4" />
                {errors.consent}
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
                Inscription en cours...
              </div>
            ) : (
              "Créer mon Compte"
            )}
          </button>

          {/* Login Link */}
          <div className="mt-6 text-center">
            <p className="text-sm text-white font-text">
              Tu as déjà un compte ?{" "}
              <a href="/login" className="font-semibold transition-colors text-secondary-50 hover:text-primary-100">
                Connecte-toi
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}