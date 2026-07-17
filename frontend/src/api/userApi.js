import apiClient from "./apiClient";

export const userApi = {
  getById: (id) => apiClient.get(`/kullanicilar/${id}`),
  getProfile: (id) => apiClient.get(`/kullanicilar/${id}/profil`),
};