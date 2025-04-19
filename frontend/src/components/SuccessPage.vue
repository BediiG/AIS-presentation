<template>
  <div class="container mt-5 text-center">
    <h1 v-if="authenticated">Welcome, {{ username }}</h1>
    <p v-if="message" class="text-success">{{ message }}</p>
    <div class="card mt-4">
      <div class="card-body">
        <h5 class="card-title">Your Token Details</h5>
        <table class="table">
          <tbody>
            <tr>
              <th>Token Type</th>
              <td>Access Token</td>
            </tr>
            <tr>
              <th>Issued At</th>
              <td>{{ formatTimestamp(tokenDetails.iat) }}</td>
            </tr>
            <tr>
              <th>Expires At</th>
              <td>{{ formatTimestamp(tokenDetails.exp) }}</td>
            </tr>
            <tr>
              <th>Remaining Time</th>
              <td>{{ calculateRemainingTime(tokenDetails.exp) }}</td>
            </tr>
            <tr>
              <th>Subject (User ID)</th>
              <td>{{ tokenDetails.sub }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <button v-if="authenticated" @click="logout" class="btn btn-danger mt-3">Logout</button>
  </div>
</template>


<script>
import { makeAuthenticatedRequest, refreshAccessToken } from "../auth";
import {jwtDecode} from "jwt-decode";

export default {
  data() {
    return {
      authenticated: false,
      username: "",
      message: "",
      tokenDetails: {}, // Store decoded token details
    };
  },
  async mounted() {
    await this.validateToken();
  },
  methods: {
    async validateToken() {
      try {
        let token = localStorage.getItem("access_token");

        // If access token is missing, try refreshing it
        if (!token) {
          token = await refreshAccessToken();
        }

        // Fetch user data using the access token
        const response = await makeAuthenticatedRequest({
          method: "GET",
          url: "http://127.0.0.1:5000/protected",
        });

        // Extract user info and token details
        this.authenticated = true;
        this.message = response.data.message;
        this.username = response.data.message.split(" ")[1]; 

        // Decode the token to extract its details
        this.tokenDetails = jwtDecode(token);
      } catch (error) {
        console.error("Error validating token:", error.response?.data || error.message);
        this.authenticated = false;

        // Redirect to login if validation fails
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        this.$router.push("/");
      }
    },
    formatTimestamp(timestamp) {
      // Convert UNIX timestamp to a human-readable format
      const date = new Date(timestamp * 1000); // Multiply by 1000 to convert seconds to milliseconds
      return date.toLocaleString(); // Format as local date and time
    },
    calculateRemainingTime(expiration) {
      const now = Math.floor(Date.now() / 1000); // Current time in seconds
      const remaining = expiration - now;

      if (remaining <= 0) {
        return "Expired";
      }

      const minutes = Math.floor(remaining / 60);
      const seconds = remaining % 60;
      return `${minutes}m ${seconds}s`;
    },
    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      this.$router.push("/");
    },
  },
};
</script>


<style>
.container {
  max-width: 700px;
}
.card {
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}
.table th {
  text-align: left;
  width: 40%;
}
.table td {
  text-align: left;
}
</style>
