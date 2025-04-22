<template>
  <div class="container mt-5 text-center">
    <h1 v-if="authenticated">Welcome, {{ username }}</h1>
    <p v-if="message" class="text-success">{{ message }}</p>

    <div v-if="!USE_COOKIES" class="card mt-4">
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
import { jwtDecode } from "jwt-decode";

const USE_COOKIES = true;

export default {
  data() {
    return {
      authenticated: false,
      username: "",
      message: "",
      tokenDetails: {},
      USE_COOKIES: USE_COOKIES, // expose to template
    };
  },
  async mounted() {
    await this.validateToken();
  },
  methods: {
    async validateToken() {
      try {
        let token;

        if (!USE_COOKIES) {
          token = localStorage.getItem("access_token");
          if (!token) {
            token = await refreshAccessToken();
          }
        }

        const response = await makeAuthenticatedRequest({
          method: "GET",
          url: "https://localhost:5000/protected",
        });

        this.authenticated = true;
        this.message = response.data.message;
        this.username = response.data.message.split(" ")[1];

        if (!USE_COOKIES && token) {
          this.tokenDetails = jwtDecode(token);
        }
      } catch (error) {
        console.error("Token validation failed:", error.response?.data || error.message);
        this.authenticated = false;
        this.clearTokens();
        this.$router.push("/");
      }
    },
    formatTimestamp(timestamp) {
      const date = new Date(timestamp * 1000);
      return date.toLocaleString();
    },
    calculateRemainingTime(exp) {
      const now = Math.floor(Date.now() / 1000);
      const remaining = exp - now;
      if (remaining <= 0) return "Expired";
      const minutes = Math.floor(remaining / 60);
      const seconds = remaining % 60;
      return `${minutes}m ${seconds}s`;
    },
    logout() {
      this.clearTokens();
      this.$router.push("/");
    },
    clearTokens() {
      if (!USE_COOKIES) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
      } else {
        // For cookie-based logout, optionally call backend /logout endpoint
        fetch("https://localhost:5000/logout", {
          method: "POST",
          credentials: "include",
        });
      }
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
