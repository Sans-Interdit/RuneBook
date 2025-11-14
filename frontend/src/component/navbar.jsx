import React from "react";
import { Link } from "react-router-dom";
import logo from "/assets/logo.png"; // chemin relatif depuis navbar.jsx

export const Navbar = () => {
  return (
    <nav className="flex h-24 bg-primary-50">
      <div className="flex flex-row items-center justify-between w-full h-full">
        <div className="flex flex-row items-center justify-between p-6 text-2xl font-semibold space-x-14 text-primary-100">
          <Link to="/">
            <img className="h-20" src={logo} alt="logo"></img>
          </Link>
          <Link to="/">
            Inscription
          </Link>
          <Link to="/">
            Inscription
          </Link>
          <Link to="/">
            Inscription
          </Link>
        </div>
        <div className="p-6 text-2xl font-semibold space-x-14 text-primary-100">
          <Link to="/demo">
            Inscription
          </Link>
          <Link to="/demo">
            Connexion
          </Link>
        </div>
      </div>
    </nav>
  );
};
