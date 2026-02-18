import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';

import Home from './pages/home';
import Catalog from './pages/catalog'
import Chatbot from './pages/chatbot'
import WorldMap from './pages/worldmap'
import Connexion from './pages/login'
import Inscription from './pages/inscription'
import Privacy from './pages/privacy';
import Logout from './pages/logout';

import { AppProvider } from "./context/appContext";

import { Navbar } from "./component/navbar";
import Terms from './pages/terms';


function AppContent() {
  const location = useLocation();

  // Ne pas afficher le Navbar sur la page /map
  const showNavbar = location.pathname !== "/map";

  return (
    <div className="flex flex-col min-h-screen">
      {showNavbar && <Navbar />}

      <main className="flex flex-col flex-1 min-h-0">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/catalog" element={<Catalog />} />
          <Route path="/chatbot" element={<Chatbot />} />
          <Route path="/map" element={<WorldMap />} />
          <Route path="/login" element={<Connexion />} />
          <Route path="/inscription" element={<Inscription />} />
          <Route path="/privacy" element={<Privacy />} />
          <Route path="/terms" element={<Terms />} />
          <Route path="/logout" element={<Logout />} />
        </Routes>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <AppProvider>
      <Router>
        <AppContent />
      </Router>
    </AppProvider>
  );
}