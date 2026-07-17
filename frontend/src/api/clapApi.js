import apiClient from "./apiClient";

export const clapApi = {
  clap: (postId) => apiClient.post("/claplar", { post_id: postId }),
  getCount: (postId) => apiClient.get(`/yazilar/${postId}/clap-sayisi`),
};