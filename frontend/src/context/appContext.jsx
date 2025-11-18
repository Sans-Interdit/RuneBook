import { createContext, useContext, useState, useEffect } from "react";
import { test } from "../api/test";

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [guides, setGuides] = useState([]);

  // Exemple d'appel API
  useEffect(() => {
    test()
      .then((data) => setGuides(data.data))
      .catch((err) => console.error(err));
  }, []);

  // Tu peux aussi stocker d'autres données globales ici
  const [user, setUser] = useState(null);

  // Les "actions" deviennent juste des fonctions normales
  const login = (name) => setUser({ name });
  const logout = () => setUser(null);

  return (
    <AppContext.Provider value={{ guides, user, login, logout }}>
      {children}
    </AppContext.Provider>
  );
};

// Hook custom pour simplifier l’accès
export const useAppContext = () => useContext(AppContext);
