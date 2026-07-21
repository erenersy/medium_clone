import apiClient from "./apiClient";

export const postApi = {
  getPublished: () => apiClient.get("/yazilar"),
  getMine: () => apiClient.get("/yazilar/benim"),
  getById: (id) => apiClient.get(`/yazilar/${id}`),
  create: (baslik, icerik) => apiClient.post("/yazilar", { baslik, icerik }),
  update: (id, veri) => apiClient.put(`/yazilar/${id}`, veri),
  remove: (id) => apiClient.delete(`/yazilar/${id}`),
  addTags: (id, etiketIsimleri) =>
    apiClient.post(`/yazilar/${id}/etiketler`, etiketIsimleri),
  getFeatured: () => apiClient.get("/yazilar/one-cikanlar"),
  uploadCover: (id, dosya) => {
  const formData = new FormData();
  formData.append("dosya", dosya);
  return apiClient.post(`/yazilar/${id}/kapak-resmi`, formData);
},
  getByTag: (etiketIsim) => apiClient.get(`/yazilar/etiket/${etiketIsim}`),
  removeTag: (id, etiketIsim) => apiClient.delete(`/yazilar/${id}/etiketler/${etiketIsim}`),
};

