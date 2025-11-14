import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import HomePage from './pages/homePage';
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
              <Route path="/" element={<HomePage />} />
            </Routes>
          </main>
        </Router>
      </div>
    </AppProvider>
  );
}
