import axios from "axios";

export async function refreshAccessToken() {
    try {
      const refreshToken = localStorage.getItem("refresh_token");
      if (!refreshToken) {
        throw new Error("Refresh token is missing");
      }
  
      const response = await axios.post("http://127.0.0.1:5000/refresh", null, {
        headers: {
          Authorization: `Bearer ${refreshToken}`,
        },
      });
  
      const { access_token } = response.data;
  
      // Save the new access token
      localStorage.setItem("access_token", access_token);
  
      return access_token;
    } catch (error) {
      console.error("Error refreshing access token:", error.response?.data || error.message);
      throw error;
    }
  }
  

  export async function makeAuthenticatedRequest(config) {
    try {
      let token = localStorage.getItem("access_token");
      if (!token) {
        throw new Error("Access token is missing");
      }
  
      config.headers = {
        ...config.headers,
        Authorization: `Bearer ${token}`, // Use the access token here
      };
  
      return await axios(config);
    } catch (error) {
      if (error.response && error.response.status === 401) {
        // Access token expired; try refreshing it
        try {
          const newAccessToken = await refreshAccessToken(); // Refresh the access token
          config.headers.Authorization = `Bearer ${newAccessToken}`; // Update header with the new access token
          return await axios(config); // Retry the original request
        } catch (refreshError) {
          console.error("Error refreshing token:", refreshError);
          // Clear tokens and redirect to login
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          throw refreshError;
        }
      }
  
      // For other errors, throw them
      throw error;
    }
  }
  
  
