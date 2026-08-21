import { useState, useEffect } from "react";
import {
  Mail,
  Lock,
  CheckCircle,
  AlertCircle,
  Eye,
  EyeOff,
  User,
} from "lucide-react";
import { useAppContext } from "../context/appContext";
import { getEmail, changeEmail, changePassword } from "../api/user";
import { useNavigate, Link } from "react-router-dom";

export default function Profile() {
  const { user } = useAppContext();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    email: "",
    newPassword: "",
    confirmPassword: "",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const [isSubmittingEmail, setIsSubmittingEmail] = useState(false);
  const [isSubmittingPassword, setIsSubmittingPassword] = useState(false);
  const [submitSuccessEmail, setSubmitSuccessEmail] = useState(false);
  const [submitSuccessPassword, setSubmitSuccessPassword] = useState(false);

  const getPasswordStrength = (password) => {
    if (!password) return { strength: 0, label: "", color: "" };

    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;

    if (strength <= 2)
      return { strength, label: "Faible", color: "bg-red-400" };
    if (strength <= 3)
      return { strength, label: "Moyen", color: "bg-secondary-50" };
    if (strength <= 4)
      return { strength, label: "Fort", color: "bg-primary-100" };
    return { strength, label: "Très Fort", color: "bg-primary-100" };
  };

  const passwordStrength = getPasswordStrength(formData.newPassword);

  useEffect(() => {
    async function fetchEmail() {
      if (user) {
        const userEmail = await getEmail();
        setFormData((prev) => ({
          ...prev,
          email: userEmail,
        }));
      } else {
        navigate("/login");
      }
    }
    fetchEmail();
  }, [user]);

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
    
    if (name == "email") {
      setSubmitSuccessEmail(false);
    }
    if (name == "newPassword" || name == "confirmPassword") {
      setSubmitSuccessPassword(false);
    }
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: "" }));
    }
  };

  const handleSubmitEmail = async (e) => {
    setSubmitSuccessEmail(false);
    e.preventDefault();

    const newErrors = {};

    if (!validateEmail(formData.email)) {
      newErrors.email = "Format d'email invalide";
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsSubmittingEmail(true);

    try {
      await changeEmail(formData.email);

      setSubmitSuccessEmail(true);
    } catch (error) {
      if (error.response.data.detail === "Cet email est déjà utilisé.") {
        setErrors({ email: error.response.data.detail });
      } else {
        setErrors({ email: "Erreur serveur\nVeuillez réessayer plus tard" });
      }
    } finally {
      setIsSubmittingEmail(false);
    }
  };

  const handleSubmitPassword = async (e) => {
    setSubmitSuccessPassword(false);
    e.preventDefault();

    const newErrors = {};

    if (passwordStrength.strength <= 3) {
      newErrors.newPassword = "Le mot de passe doit être au moins fort";
    }

    if (formData.newPassword !== formData.confirmPassword) {
      newErrors.confirmPassword = "Les mots de passe ne correspondent pas";
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsSubmittingPassword(true);

    try {
      changePassword(formData.newPassword);

      setSubmitSuccessPassword(true);
      setFormData((prev) => ({
        ...prev,
        newPassword: "",
        confirmPassword: "",
      }));
    } catch (error) {
      setErrors({ password: "Erreur serveur\nVeuillez réessayer plus tard" });
    } finally {
      setIsSubmittingPassword(false);
    }
  };

  return (
    <div className="flex items-start justify-center flex-1 px-6 py-20 overflow-auto bg-primary-50">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="flex items-center justify-center w-16 h-16 mx-auto mb-4 rounded-full bg-primary-100">
            <User className="w-8 h-8 text-primary-50" />
          </div>
          <h1 className="mb-2 text-5xl font-bold text-secondary-50 font-titre">
            Mon Profil
          </h1>
          <p className="text-xl text-white font-text">
            Gère tes informations de compte
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
            <div className="relative mb-4">
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
            {/* Success message */}
            {submitSuccessEmail && (
              <div className="flex items-center gap-2 p-4 mb-6 text-sm border-2 rounded-lg text-secondary-50 bg-secondary-50/10 border-secondary-50/30">
                <CheckCircle className="w-5 h-5" />
                Profil mis à jour avec succès !
              </div>
            )}
          </div>
          {/* Save Button */}
          <button
            type="button"
            onClick={handleSubmitEmail}
            disabled={isSubmittingEmail || !formData.email}
            className="w-full py-2 text-2xl font-bold text-black transition-all duration-300 rounded-lg bg-secondary-50 hover:scale-105 hover:shadow-xl hover:shadow-secondary-50/30 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
          >
            {isSubmittingEmail ? (
              <div className="flex items-center justify-center gap-2">
                <div className="w-5 h-5 border-2 rounded-full border-primary-50 border-t-transparent animate-spin"></div>
                Enregistrement...
              </div>
            ) : (
              "Sauvegarder"
            )}
          </button>
        </div>
        <div className="p-8 mt-6 border-2 rounded-2xl bg-primary-50 border-primary-100/30">
          {/* New Password Field */}
          <div className="mb-6">
            <label
              htmlFor="newPassword"
              className="block mb-2 text-sm font-semibold text-secondary-50 font-text"
            >
              Nouveau Mot de Passe
            </label>
            <div className="relative">
              <Lock className="absolute w-5 h-5 text-white transform -translate-y-1/2 left-4 top-1/2" />
              <input
                type={showPassword ? "text" : "password"}
                id="newPassword"
                name="newPassword"
                autoComplete="new-password"
                value={formData.newPassword}
                onChange={handleInputChange}
                maxLength={200}
                placeholder="Le nouveau mot de passe"
                className={`w-full py-3 pl-12 pr-12 text-white transition-all duration-300 border-2 rounded-lg bg-primary-50 placeholder-white/50 focus:outline-none font-text ${
                  errors.newPassword
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
            {formData.newPassword && (
              <div className="mt-2">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs text-white">
                    Force du mot de passe
                  </span>
                  <span
                    className={`text-xs font-semibold ${passwordStrength.color.replace("bg-", "text-")}`}
                  >
                    {passwordStrength.label}
                  </span>
                </div>
                <div className="h-2 overflow-hidden rounded-full bg-primary-100/30">
                  <div
                    className={`h-full transition-all duration-300 ${passwordStrength.color}`}
                    style={{
                      width: `${(passwordStrength.strength / 5) * 100}%`,
                    }}
                  ></div>
                </div>
              </div>
            )}
            {errors.newPassword && (
              <div className="flex items-center gap-1 mt-2 text-sm text-red-400">
                <AlertCircle className="w-4 h-4" />
                {errors.newPassword}
              </div>
            )}
          </div>

          {/* Confirm Password Field */}
          <div className="mb-6">
            <label
              htmlFor="confirmPassword"
              className="block mb-2 text-sm font-semibold text-secondary-50 font-text"
            >
              Confirme le Mot de Passe
            </label>
            <div className="relative mb-4">
              <Lock className="absolute w-5 h-5 text-white transform -translate-y-1/2 left-4 top-1/2" />
              <input
                type={showConfirmPassword ? "text" : "password"}
                id="confirmPassword"
                name="confirmPassword"
                autoComplete="new-password"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                maxLength={200}
                placeholder="Répète le nouveau mot de passe"
                className={`w-full py-3 pl-12 pr-12 text-white transition-all duration-300 border-2 rounded-lg bg-primary-50 placeholder-white/50 focus:outline-none font-text ${
                  errors.confirmPassword
                    ? "border-red-400 focus:border-red-400"
                    : "border-primary-100/30 focus:border-secondary-50"
                }`}
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute text-white transform -translate-y-1/2 right-4 top-1/2 hover:text-secondary-50"
              >
                {showConfirmPassword ? (
                  <Eye className="w-5 h-5" />
                ) : (
                  <EyeOff className="w-5 h-5" />
                )}
              </button>
            </div>
            {errors.confirmPassword && (
              <div className="flex items-center gap-1 mt-2 text-sm text-red-400">
                <AlertCircle className="w-4 h-4" />
                {errors.confirmPassword}
              </div>
            )}
            {/* Success message */}
            {submitSuccessPassword && (
              <div className="flex items-center gap-2 p-4 mb-6 text-sm border-2 rounded-lg text-secondary-50 bg-secondary-50/10 border-secondary-50/30">
                <CheckCircle className="w-5 h-5" />
                Profil mis à jour avec succès !
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

          {/* Save Button */}
          <button
            type="button"
            onClick={handleSubmitPassword}
            disabled={
              isSubmittingPassword ||
              !formData.newPassword ||
              !formData.confirmPassword
            }
            className="w-full py-2 text-2xl font-bold text-black transition-all duration-300 rounded-lg bg-secondary-50 hover:scale-105 hover:shadow-xl hover:shadow-secondary-50/30 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
          >
            {isSubmittingPassword ? (
              <div className="flex items-center justify-center gap-2">
                <div className="w-5 h-5 border-2 rounded-full border-primary-50 border-t-transparent animate-spin"></div>
                Enregistrement...
              </div>
            ) : (
              "Sauvegarder"
            )}
          </button>
        </div>

        {/* Danger zone */}
        <div className="p-8 mt-6 border-2 rounded-2xl bg-primary-50 border-red-400/30">
          <Link
            to="/logout"
            className="flex items-center justify-center py-3 mb-6 text-2xl font-bold text-black transition-all duration-300 bg-orange-500 rounded-lg hover:scale-105 hover:shadow-xl hover:shadow-secondary-50/30 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
          >
            Se Déconnecter
          </Link>

          <Link
            to="/suppr-acc"
            className="flex items-center justify-center py-3 text-2xl font-bold text-black transition-all duration-300 bg-red-500 rounded-lg hover:scale-105 hover:shadow-xl hover:shadow-secondary-50/30 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
          >
            <span> Supprimer mon Compte</span>
          </Link>
        </div>
      </div>
    </div>
  );
}
