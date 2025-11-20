import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Home from './pages/home';
import Catalog from './pages/catalog'
import Chatbot from './pages/chatbot'
import Connexion from './pages/login'
import Inscription from './pages/inscription'
import Privacy from './pages/privacy';

import { AppProvider } from "./context/appContext";

import { Navbar } from "./component/navbar";
import Terms from './pages/terms';

export default function App() {
  return (
    <AppProvider>
      <div className="flex flex-col min-h-screen">
        <Router>
          <Navbar />
          <main className="flex flex-col flex-1">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/catalog" element={<Catalog />} />
              <Route path="/chatbot" element={<Chatbot />} />
              <Route path="/login" element={<Connexion />} />
              <Route path="/inscription" element={<Inscription />} />
              <Route path="/privacy" element={<Privacy />} />
              <Route path="/terms" element={<Terms />} />
            </Routes>
          </main>
        </Router>
      </div>
    </AppProvider>
  );
}
