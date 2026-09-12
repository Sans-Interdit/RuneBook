import { useState, useEffect } from "react";
import {
  Home,
  BookOpen,
  MessageSquare,
  UserPlus,
  LogIn,
  Menu,
  X,
  LogOut,
  User,
} from "lucide-react";
import { Link } from "react-router-dom";
import logo from "/assets/logo.webp";
import { useLocation } from "react-router-dom";
import { useAppContext } from "../context/appContext";

export const Navbar = () => {
  const { user } = useAppContext();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const [navLinks, setNavLinks] = useState([
    { to: "/", label: "Accueil", icon: <Home className="w-6 h-6" /> },
    {
      to: "/catalog",
      label: "Catalogue",
      icon: <BookOpen className="w-6 h-6" />,
    },
  ]);

  const [authLinks, setAuthLinks] = useState([
    {
      to: "/inscription",
      label: "Inscription",
      icon: <UserPlus className="w-6 h-6" />,
    },
    { to: "/login", label: "Connexion", icon: <LogIn className="w-6 h-6" /> },
  ]);

  useEffect(() => {
    const verifyConnexion = async () => {
      if (user) {
        setNavLinks((links) => {
          return [
            ...navLinks,
            {
              to: "/chatbot",
              label: "Chatbot",
              icon: <MessageSquare className="w-6 h-6" />,
            },
          ];
        });
        setAuthLinks((links) => {
          return [
            {
              to: "/profile",
              label: "Mon compte",
              icon: <User/> ,
            }
          ];
        });
      } else {
        setNavLinks((links) => {
          return [
            { to: "/", label: "Accueil", icon: <Home className="w-6 h-6" /> },
            {
              to: "/catalog",
              label: "Catalogue",
              icon: <BookOpen className="w-6 h-6" />,
            },
          ];
        });
        setAuthLinks((links) => {
          return [
            {
              to: "/inscription",
              label: "Inscription",
              icon: <UserPlus className="w-6 h-6" />,
            },
            {
              to: "/login",
              label: "Connexion",
              icon: <LogIn className="w-6 h-6" />,
            },
          ];
        });
      }
    };
    verifyConnexion();
  }, [user]);

  return (
    <nav className="z-50 h-20 shadow-lg nav-background shadow-primary-100/20">
      <div className="flex items-center justify-between h-20 px-6 mx-auto">
        {/* Logo */}
        <Link to="/" className="relative z-10">
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center h-16 w-26">
              <img className="h-16" src={logo} alt="logo"></img>
            </div>
            <span className="hidden text-3xl font-bold text-transparent md:block bg-clip-text bg-primary-100 font-titre">
              RuneBook
            </span>
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <div className="flex items-center space-x-2">
          {navLinks.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              className={`
                relative px-4 py-2 text-xl font-bold rounded-xl transition-all duration-300
                flex items-center space-x-2 group
                ${
                  location.pathname === link.to
                    ? "text-primary-50 bg-secondary-50 shadow-lg"
                    : "text-primary-100 hover:text-primary-50 hover:bg-primary-100"
                }
              `}
            >
              <span className="transition-transform duration-300 group-hover:scale-110">
                {link.icon}
              </span>
              <span>{link.label}</span>
            </Link>
          ))}
        </div>

        {/* Desktop Auth Buttons */}
        <div className="flex items-center space-x-4">
          {authLinks.map((link, index) => (
            <Link
              key={link.to}
              to={link.to}
              className={`
                px-4 py-2 text-xl font-bold rounded-xl transition-all duration-300
                flex items-center space-x-2 group
                ${
                  index === 0
                    ? "border-2 border-primary-100 hover:text-primary-100 bg-primary-100 hover:bg-transparent text-primary-50 hover:scale-105"
                    : "border-2 rounded-lg border-secondary-50  bg-secondary-50 hover:bg-transparent hover:text-secondary-50 text-primary-50 hover:scale-105"
                }
              `}
            >
              <span className="transition-transform duration-300 group-hover:scale-110">
                {link.icon}
              </span>
              <span>{link.label}</span>
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
};
