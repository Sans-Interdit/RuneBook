import { createContext, useContext, useState, useEffect } from "react";
import { login, register, logout, getId } from "../api/user";
import { getGuides } from "../api/guide"

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [guides, setGuides] = useState([]);

  const getIdContext = () => {
    return getId()
    .then(res => {
      // console.log(res.data);
      return res.data;
    })
    .catch(err => {
      if (err?.response?.status === 401) {
        // on ignore complètement l'erreur 401
        return null; 
      }

      // on log uniquement les erreurs qui ne sont pas des 401
      console.error(err);
      return null;
    });
  }
  // Exemple d'appel API
  useEffect(() => {
    getGuides()
    .then((data) => setGuides(data.data))
    .catch((err) => {
      setGuides([])
      console.error(err);
    });
  }, []);

  const registerContext = async (email, password) => {
    await register(email, password);
  };

  const loginContext = async (email, password) => {
    try {
      await login(email, password);
    } catch (error) {
      if (error.response?.status === 401) {
        throw new Error("INVALID_CREDENTIALS");
      }
      throw new Error("SERVER_ERROR");
    }
  };


  const logoutContext = async () => {
    await logout();
  };

  return (
    <AppContext.Provider value={{ guides, getIdContext, loginContext, logoutContext, registerContext }}>
      {children}
    </AppContext.Provider>
  );
};

// Hook custom pour simplifier l’accès
export const useAppContext = () => useContext(AppContext);
