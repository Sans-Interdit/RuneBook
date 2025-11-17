import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Home from './pages/home';
import Catalog from './pages/catalogue'
import Chatbot from './pages/chatbot'
import Connexion from './pages/connexion'
import Inscription from './pages/inscription'

import { AppProvider } from "./context/appContext";

import { Navbar } from "./component/navbar";

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
              <Route path="/connexion" element={<Connexion />} />
              <Route path="/inscription" element={<Inscription />} />
            </Routes>
          </main>
        </Router>
      </div>
    </AppProvider>
  );
}
