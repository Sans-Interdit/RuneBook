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
} from "lucide-react";
import { Link } from "react-router-dom";
import logo from "/assets/logo.png"; // chemin relatif depuis navbar.jsx
import { useLocation } from "react-router-dom";
import { useAppContext } from "../context/appContext";

export const Navbar = () => {
  const { user } = useAppContext();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const [navLinks, setNavLinks] = useState([
    { to: "/", label: "Accueil", icon: <Home className="w-5 h-5" /> },
    {
      to: "/catalog",
      label: "Catalogue",
      icon: <BookOpen className="w-5 h-5" />,
    },
  ]);

  const [authLinks, setAuthLinks] = useState([
    {
      to: "/inscription",
      label: "Inscription",
      icon: <UserPlus className="w-5 h-5" />,
    },
    { to: "/login", label: "Connexion", icon: <LogIn className="w-5 h-5" /> },
  ]);

  useEffect(() => {
    const verifyConnexion = async () => {
      console.log(user);
      if (user) {
        console.log("co");
        setNavLinks((links) => {
          return [
            ...navLinks,
            {
              to: "/chatbot",
              label: "Chatbot",
              icon: <MessageSquare className="w-5 h-5" />,
            },
          ];
        });
        setAuthLinks((links) => {
          return [
            {
              to: "/logout",
              label: "Déconnection",
              icon: <LogOut className="w-5 h-5" />,
            },
          ];
        });
      } else {
        setNavLinks((links) => {
          return [
            { to: "/", label: "Accueil", icon: <Home className="w-5 h-5" /> },
            {
              to: "/catalog",
              label: "Catalogue",
              icon: <BookOpen className="w-5 h-5" />,
            },
          ];
        });
        setAuthLinks((links) => {
          return [
            {
              to: "/inscription",
              label: "Inscription",
              icon: <UserPlus className="w-5 h-5" />,
            },
            {
              to: "/login",
              label: "Connexion",
              icon: <LogIn className="w-5 h-5" />,
            },
          ];
        });
      }
    };
    verifyConnexion();
  }, [user]);

  return (
    <nav className="z-50 h-20 shadow-lg nav-background shadow-primary-100/20">
      <div className="flex items-center justify-between h-20 px-6 mx-auto max-w-7xl">
        {/* Logo */}
        <Link to="/" className="relative z-10">
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center h-16 w-26">
              <img className="h-16" src={logo} alt="logo"></img>
            </div>
            <span className="hidden text-2xl font-bold text-transparent md:block bg-clip-text bg-primary-100 font-titre">
              RuneBook
            </span>
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <div className="items-center hidden space-x-2 lg:flex">
          {navLinks.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              className={`
                relative px-4 py-2 text-lg font-semibold rounded-xl transition-all duration-300 font-text
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
        <div className="items-center hidden space-x-4 lg:flex">
          {authLinks.map((link, index) => (
            <Link
              key={link.to}
              to={link.to}
              className={`
                px-4 py-2 text-lg font-semibold rounded-xl transition-all duration-300 font-text
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

        {/* Mobile Menu Button */}
        <button
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          className="z-10 p-2 transition-colors rounded-lg lg:hidden text-primary-100 hover:bg-primary-100/20"
        >
          {isMenuOpen ? (
            <X className="w-8 h-8" />
          ) : (
            <Menu className="w-8 h-8" />
          )}
        </button>
      </div>

      {/* Mobile Menu */}
      <div
        className={`
          lg:hidden absolute top-24 left-0 right-0 bg-gradient-to-br from-primary-50 to-background-50
          border-t-2 border-primary-100/30 shadow-2xl transition-all duration-300 overflow-hidden
          ${isMenuOpen ? "max-h-screen opacity-100" : "max-h-0 opacity-0"}
        `}
      >
        <div className="px-6 py-6 space-y-3">
          {navLinks.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              onClick={() => {
                setIsMenuOpen(false);
              }}
              className={`
                flex items-center space-x-3 px-6 py-4 rounded-xl transition-all duration-300 font-text text-lg font-semibold
                ${
                  location.pathname === link.to
                    ? "bg-gradient-to-r from-primary-100 to-secondary-50 text-primary-50 shadow-lg"
                    : "text-primary-100 hover:bg-primary-100/20"
                }
              `}
            >
              {link.icon}
              <span>{link.label}</span>
            </Link>
          ))}

          <div className="pt-4 mt-4 space-y-3 border-t-2 border-primary-100/30">
            {authLinks.map((link, index) => (
              <Link
                key={link.to}
                to={link.to}
                onClick={() => {
                  setIsMenuOpen(false);
                }}
                className={`
                  flex items-center justify-center space-x-3 px-6 py-4 rounded-xl transition-all duration-300 font-text text-lg font-semibold
                  ${
                    index === 0
                      ? "border-2 border-primary-100 text-primary-100 hover:bg-primary-100 hover:text-primary-50"
                      : "bg-gradient-to-r from-primary-100 to-secondary-50 text-primary-50 hover:shadow-lg"
                  }
                `}
              >
                {link.icon}
                <span>{link.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
};
