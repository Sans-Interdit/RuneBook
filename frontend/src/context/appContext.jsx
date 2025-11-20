import { createContext, useContext, useState, useEffect } from "react";
import { login, register } from "../api/user";
import { getGuides } from "../api/guides"

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [guides, setGuides] = useState([]);
  const [token, setToken] = useState(null);

  // Exemple d'appel API
  useEffect(() => {
    getGuides()
      .then((data) => setGuides(data.data))
      .catch((err) => console.error(err));
  }, []);

  const registerContext = (email, password) => {
    localStorage.setItem("AuthToken" , register(email, password));
  };

  const loginContext = (email, password) => {
    localStorage.setItem("AuthToken" , login(email, password));
  };

  const logoutContext = () => localStorage.removeItem("AuthToken");

  return (
    <AppContext.Provider value={{ guides, token, loginContext, logoutContext, registerContext }}>
      {children}
    </AppContext.Provider>
  );
};

// Hook custom pour simplifier l’accès
export const useAppContext = () => useContext(AppContext);
