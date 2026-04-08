import { Link } from "react-router-dom";

export const Footer = () => (
  <footer className="px-6 py-10 border-t border-primary-100/20 bg-background-50">
    <div className="flex flex-col items-center gap-6 mx-auto max-w-7xl">
      {/* Brand */}
      <div className="flex flex-col items-center gap-2">
        <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-secondary-50 font-titre">
          RuneBook
        </h2>
        <p className="text-sm italic text-secondary-50/70 font-text">
          Where League of Legends feel logical
        </p>
      </div>

      {/* Nav links */}
      <nav className="flex gap-8">
        {[
          { label: "Home", to: "/" },
          { label: "Catalog", to: "/catalog" },
          { label: "Privacy", to: "/privacy" },
          { label: "Legal Terms", to: "/terms" },
        ].map(({ label, to }) => (
          <Link
            key={to}
            to={to}
            className="text-sm font-semibold transition-all duration-200 text-white/70 font-text hover:text-secondary-50"
          >
            {label}
          </Link>
        ))}
      </nav>

      {/* Divider */}
      <div className="w-full h-px bg-primary-100/20" />

      {/* Copyright + disclaimer */}
      <div className="flex flex-col items-center gap-3 text-center">
        <p className="text-xs text-white/60 font-text">
          © 2026 · Fait par Yanis Bouchilloux
        </p>
        <p className="max-w-2xl text-xs leading-relaxed text-white/60 font-text">
          Runebook is a fan-made project and is not affiliated with, endorsed,
          sponsored, or specifically approved by Riot Games. Riot Games and all
          associated properties are trademarks or registered trademarks of Riot
          Games, Inc.
        </p>
      </div>
    </div>
  </footer>
);
