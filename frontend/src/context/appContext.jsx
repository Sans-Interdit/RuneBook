import { createContext, useContext, useState, useEffect } from "react";
import { login, register, logout, getId } from "../api/user";

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    console.log(user)
    const fetchUser = async () => {
      try {
        const res = await getId();
        setUser(res.data.id_user);
      } catch (err) {
        if (err?.response?.status === 401) {
          setUser(null); // pas connecté
        } else {
          console.error(err);
        }
      }
      setIsLoading(false);
    };

    fetchUser();
  }, []);

  const registerContext = async (email, password) => {
    try {
      const response = await register(email, password);
      setUser(response.data.id_account);
    } catch (error) {
      if (error.response?.status === 409) {
        throw new Error("EMAIL_USED");
      }
      throw new Error("SERVER_ERROR");
    }
  };

  const loginContext = async (email, password) => {
    try {
      const response = await login(email, password);
      setUser(response.data.id_account);
    } catch (error) {
      if (error.response?.status === 401) {
        throw new Error("INVALID_CREDENTIALS");
      }
      throw new Error("SERVER_ERROR");
    }
  };


  const logoutContext = async () => {
    await logout();
    setUser(null);
  };

  return (
    <AppContext.Provider value={{ user, isLoading, loginContext, logoutContext, registerContext }}>
      {children}
    </AppContext.Provider>
  );
};

// Hook custom pour simplifier l’accès
export const useAppContext = () => useContext(AppContext);
