const ACCESS_TOKEN_KEY = "voice_access_token";
const REFRESH_TOKEN_KEY = "voice_refresh_token";

export const tokenService = {
  getAccessToken: () => localStorage.getItem(ACCESS_TOKEN_KEY),
  getRefreshToken: () => localStorage.getItem(REFRESH_TOKEN_KEY),
  setTokens: (accessToken, refreshToken) => {
    localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  },
  clearTokens: () => {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
  },
  getUserIdFromToken: () => {
    const token = localStorage.getItem(ACCESS_TOKEN_KEY);
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      return parseInt(payload.sub, 10);
    } catch {
      return null;
    }
  },
};