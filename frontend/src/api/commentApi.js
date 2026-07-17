import apiClient from "./apiClient";

export const commentApi = {
  create: (icerik, postId) =>
    apiClient.post("/yorumlar", { icerik, post_id: postId }),
  getForPost: (postId) => apiClient.get(`/yazilar/${postId}/yorumlar`),
  remove: (id) => apiClient.delete(`/yorumlar/${id}`),
};