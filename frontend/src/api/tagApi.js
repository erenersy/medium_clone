import apiClient from "./apiClient";

export const tagApi = {
  getAll: () => apiClient.get("/etiketler"),
};