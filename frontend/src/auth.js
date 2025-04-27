import axios from "axios";

// 🔁 Toggle between token-in-header vs. cookie-based authentication
const USE_COOKIES = true;

// 🔥 Load backend URL from environment
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

export async function refreshAccessToken() {
  if (USE_COOKIES) {
    try {
      // Hit the refresh endpoint using cookies
      await axios.post(`${BACKEND_URL}/refresh`, null, {
        withCredentials: true,
      });
    } catch (error) {
      console.error("Error refreshing token via cookie:", error.response?.data || error.message);
      throw error;
    }
  } else {
    try {
      const refreshToken = localStorage.getItem("refresh_token");
      if (!refreshToken) {
        throw new Error("Refresh token is missing");
      }

      const response = await axios.post(`${BACKEND_URL}/refresh`, null, {
        headers: {
          Authorization: `Bearer ${refreshToken}`,
        },
      });

      const { access_token } = response.data;

      // Save the new access token
      localStorage.setItem("access_token", access_token);

      return access_token;
    } catch (error) {
      console.error("Error refreshing token:", error.response?.data || error.message);
      throw error;
    }
  }
}

export async function makeAuthenticatedRequest(config) {
  try {
    if (USE_COOKIES) {
      return await axios({
        ...config,
        withCredentials: true, // ✅ Include cookies
        url: `${BACKEND_URL}${config.url}`, // ✅ Prefix the backend URL
      });
    } else {
      let token = localStorage.getItem("access_token");
      if (!token) {
        throw new Error("Access token is missing");
      }

      config.headers = {
        ...config.headers,
        Authorization: `Bearer ${token}`, // ✅ Send in header
      };
      config.url = `${BACKEND_URL}${config.url}`; // ✅ Prefix the backend URL
      return await axios(config);
    }
  } catch (error) {
    // Retry if token expired (only relevant in header mode)
    if (!USE_COOKIES && error.response && error.response.status === 401) {
      try {
        const newAccessToken = await refreshAccessToken();
        config.headers.Authorization = `Bearer ${newAccessToken}`;
        config.url = `${BACKEND_URL}${config.url}`;
        return await axios(config);
      } catch (refreshError) {
        console.error("Error refreshing token:", refreshError);
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        throw refreshError;
      }
    }

    throw error;
  }
}
