import axios from "axios";
import { tokenService } from "../services/tokenService";

const BASE_URL = "http://127.0.0.1:8000";

const apiClient = axios.create({ baseURL: BASE_URL });

apiClient.interceptors.request.use((config) => {
  const token = tokenService.getAccessToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

let yenilemeIslemi = null;

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        if (!yenilemeIslemi) {
          yenilemeIslemi = axios.post(`${BASE_URL}/refresh-token`, {
            refresh_token: tokenService.getRefreshToken(),
          });
        }
        const response = await yenilemeIslemi;
        yenilemeIslemi = null;
        const { access_token, refresh_token } = response.data;
        tokenService.setTokens(access_token, refresh_token);
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return apiClient(originalRequest);
      } catch (yenilemeHatasi) {
        yenilemeIslemi = null;
        tokenService.clearTokens();
        window.location.href = "/login";
        return Promise.reject(yenilemeHatasi);
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;