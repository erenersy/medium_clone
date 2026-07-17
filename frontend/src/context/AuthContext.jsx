import { createContext, useContext, useState, useEffect } from "react";
import { tokenService } from "../services/tokenService";
import { userApi } from "../api/userApi";
import { authApi } from "../api/authApi";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [yukleniyor, setYukleniyor] = useState(true);

  useEffect(() => {
    const kullaniciYukle = async () => {
      const userId = tokenService.getUserIdFromToken();
      if (userId) {
        try {
          const response = await userApi.getById(userId);
          setUser(response.data);
        } catch {
          tokenService.clearTokens();
        }
      }
      setYukleniyor(false);
    };
    kullaniciYukle();
  }, []);

  const login = async (eposta, sifre) => {
    const response = await authApi.login(eposta, sifre);
    tokenService.setTokens(response.data.access_token, response.data.refresh_token);
    const userId = tokenService.getUserIdFromToken();
    const userResponse = await userApi.getById(userId);
    setUser(userResponse.data);
  };

  const logout = () => {
    tokenService.clearTokens();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, yukleniyor }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);