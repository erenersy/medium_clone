import apiClient from "./apiClient";

export const followApi = {
  follow: (userId) => apiClient.post(`/takip/${userId}`),
  unfollow: (userId) => apiClient.delete(`/takip/${userId}`),
  getFollowers: (userId) => apiClient.get(`/kullanicilar/${userId}/takipcileri`),
  getFollowing: (userId) => apiClient.get(`/kullanicilar/${userId}/takip-ettikleri`),
};