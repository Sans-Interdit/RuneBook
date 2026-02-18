import React, { useState } from "react";
import { Mail, Lock, CheckCircle, AlertCircle, Eye, EyeOff, LogIn } from "lucide-react";
import { useAppContext } from "../context/appContext";

export default function Login() {
  const { loginContext } = useAppContext();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    rememberMe: false
  });

  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
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
    }
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      await loginContext(formData.email, formData.password);

      window.location.href = '/chatbot';
    }
    catch (error) {
      if (error.message === "INVALID_CREDENTIALS") {
        setErrors({submit: "Email ou mot de passe incorrect"});
      }
      else {
        setErrors({submit: "Erreur serveur\nVeuillez réessayer plus tard"});
      }
    }
    finally {
      setIsSubmitting(false);
    }
  };

  if (submitSuccess) {
    return (
      <div className="flex items-center justify-center flex-1 bg-primary-50">
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
    <div className="flex items-center justify-center flex-1 px-6 bg-primary-50">
      <div className="w-full max-w-md mb-20">
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
            <div className="flex items-center justify-between mb-2">
              <label htmlFor="password" className="text-sm font-semibold text-secondary-50 font-text">
                Mot de Passe
              </label>
              <a 
                href="/forgot-password" 
                className="text-xs font-semibold transition-colors text-secondary-50 hover:text-primary-100"
              >
                Mot de passe oublié ?
              </a>
            </div>
            <div className="relative">
              <Lock className="absolute w-5 h-5 text-white transform -translate-y-1/2 left-4 top-1/2" />
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                placeholder="Entre ton mot de passe"
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
            {errors.password && (
              <div className="flex items-center gap-1 mt-2 text-sm text-red-400">
                <AlertCircle className="w-4 h-4" />
                {errors.password}
              </div>
            )}
          </div>

          {/* Remember Me Checkbox */}
          <div className="mb-6">
            <label className="flex items-center gap-3 cursor-pointer group">
              <div className="relative flex-shrink-0">
                <input
                  type="checkbox"
                  name="rememberMe"
                  checked={formData.rememberMe}
                  onChange={handleInputChange}
                  className="w-5 h-5 transition-all duration-300 border-2 rounded appearance-none cursor-pointer bg-primary-50 border-primary-100/30 checked:bg-secondary-50 checked:border-secondary-50 focus:outline-none focus:ring-2 focus:ring-secondary-50/50"
                />
                {formData.rememberMe && (
                  <CheckCircle className="absolute w-5 h-5 transform -translate-x-1/2 -translate-y-1/2 pointer-events-none text-primary-50 top-1/2 left-1/2" />
                )}
              </div>
              <span className="text-sm text-white font-text">
                Se souvenir de moi
              </span>
            </label>
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
              <a href="/inscription" className="font-semibold transition-colors text-secondary-50 hover:text-primary-100">
                Inscris-toi gratuitement
              </a>
            </p>
          </div>
        </div>

        {/* Additional Options */}
        {/* <div className="p-4 mt-6 border-2 rounded-lg bg-primary-50 border-primary-100/30">
          <p className="mb-3 text-sm font-semibold text-center text-secondary-50 font-text">
            Ou continue avec
          </p>
          <div className="grid grid-cols-2 gap-3">
            <button className="flex items-center justify-center gap-2 px-4 py-3 transition-all duration-300 border-2 rounded-lg border-primary-100/30 hover:border-secondary-50 hover:scale-105">
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path fill="#EA4335" d="M5.26620003,9.76452941 C6.19878754,6.93863203 8.85444915,4.90909091 12,4.90909091 C13.6909091,4.90909091 15.2181818,5.50909091 16.4181818,6.49090909 L19.9090909,3 C17.7818182,1.14545455 15.0545455,0 12,0 C7.27006974,0 3.1977497,2.69829785 1.23999023,6.65002441 L5.26620003,9.76452941 Z"/>
                <path fill="#34A853" d="M16.0407269,18.0125889 C14.9509167,18.7163016 13.5660892,19.0909091 12,19.0909091 C8.86648613,19.0909091 6.21911939,17.076871 5.27698177,14.2678769 L1.23746264,17.3349879 C3.19279051,21.2936293 7.26500293,24 12,24 C14.9328362,24 17.7353462,22.9573905 19.834192,20.9995801 L16.0407269,18.0125889 Z"/>
                <path fill="#4A90E2" d="M19.834192,20.9995801 C22.0291676,18.9520994 23.4545455,15.903663 23.4545455,12 C23.4545455,11.2909091 23.3454545,10.5272727 23.1818182,9.81818182 L12,9.81818182 L12,14.4545455 L18.4363636,14.4545455 C18.1187732,16.013626 17.2662994,17.2212117 16.0407269,18.0125889 L19.834192,20.9995801 Z"/>
                <path fill="#FBBC05" d="M5.27698177,14.2678769 C5.03832634,13.556323 4.90909091,12.7937589 4.90909091,12 C4.90909091,11.2182781 5.03443647,10.4668121 5.26620003,9.76452941 L1.23999023,6.65002441 C0.43658717,8.26043162 0,10.0753848 0,12 C0,13.9195484 0.444780743,15.7301709 1.23746264,17.3349879 L5.27698177,14.2678769 Z"/>
              </svg>
              <span className="text-sm font-semibold text-white">Google</span>
            </button>
            <button className="flex items-center justify-center gap-2 px-4 py-3 transition-all duration-300 border-2 rounded-lg border-primary-100/30 hover:border-secondary-50 hover:scale-105">
              <svg className="w-5 h-5" fill="white" viewBox="0 0 24 24">
                <path d="M22.46 6c-.85.38-1.78.64-2.75.76 1-.6 1.76-1.55 2.12-2.68-.93.55-1.96.96-3.06 1.18-.88-.94-2.13-1.53-3.51-1.53-2.66 0-4.81 2.16-4.81 4.81 0 .38.04.75.13 1.1-4-.2-7.57-2.12-9.95-5.04-.42.72-.66 1.55-.66 2.44 0 1.67.85 3.14 2.14 4-.79-.03-1.53-.24-2.18-.61v.06c0 2.33 1.66 4.28 3.86 4.72-.4.11-.83.17-1.27.17-.31 0-.62-.03-.92-.08.62 1.94 2.42 3.35 4.55 3.39-1.67 1.31-3.77 2.09-6.05 2.09-.39 0-.78-.02-1.17-.07 2.18 1.4 4.77 2.21 7.55 2.21 9.06 0 14-7.5 14-14 0-.21 0-.42-.02-.63.96-.69 1.8-1.56 2.46-2.55z"/>
              </svg>
              <span className="text-sm font-semibold text-white">Twitter</span>
            </button>
          </div>
        </div> */}
      </div>
    </div>
  );
}