import apiClient from "./apiClient";

export const authApi = {
  register: (isim, eposta, sifre) =>
    apiClient.post("/register", { isim, eposta, sifre }),
  login: (eposta, sifre) =>
    apiClient.post("/login", { eposta, sifre }),
};