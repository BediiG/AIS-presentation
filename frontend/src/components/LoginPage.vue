<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header text-center">
            <h2 v-if="isSignup">Sign Up</h2>
            <h2 v-else>Login</h2>
          </div>
          <div class="card-body">
            <form @submit.prevent="isSignup ? signup() : login()">
              <div class="mb-3">
                <label for="username" class="form-label">Username:</label>
                <input
                  v-model="username"
                  id="username"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password:</label>
                <input
                  v-model="password"
                  id="password"
                  type="password"
                  class="form-control"
                  required
                />
              </div>
              <div class="text-center">
                <button
                  type="submit"
                  class="btn btn-primary w-100"
                  :disabled="loading"
                >
                  {{ isSignup ? "Sign Up" : "Login" }}
                </button>
              </div>
            </form>
            <p v-if="error" class="text-danger text-center mt-3">{{ error }}</p>
            <p v-if="loading" class="text-center text-primary">Processing...</p>
          </div>
          <div class="card-footer text-center">
            <p>
              <span v-if="isSignup">Already have an account? </span>
              <span v-else>Don't have an account? </span>
              <button
                @click="toggleSignup"
                class="btn btn-link text-decoration-none"
              >
                {{ isSignup ? "Login" : "Sign Up" }}
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { refreshAccessToken } from "../auth";

const USE_COOKIES = false;

export default {
  data() {
    return {
      username: "",
      password: "",
      isSignup: false,
      error: "",
      isAuthenticated: false,
      loading: false,
    };
  },
  async mounted() {
    if (!USE_COOKIES) {
      const accessToken = localStorage.getItem("access_token");
      const refreshToken = localStorage.getItem("refresh_token");

      if (accessToken) {
        try {
          await axios.get("http://localhost:5000/protected", {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
          this.$router.push("/success");
        } catch {
          if (refreshToken) {
            try {
              await refreshAccessToken();
              this.$router.push("/success");
            } catch (refreshError) {
              this.clearTokens();
            }
          } else {
            this.clearTokens();
          }
        }
      } else if (refreshToken) {
        try {
          await refreshAccessToken();
          this.$router.push("/success");
        } catch {
          this.clearTokens();
        }
      }
    } else {
      try {
        await axios.get("http://localhost:5000/protected", {
          withCredentials: true,
        });
        this.$router.push("/success");
      } catch {
        // Not authenticated
      }
    }
  },
  methods: {
    async login() {
      if (!this.username || !this.password) {
        this.error = "Both username and password are required.";
        return;
      }
      this.loading = true;
      try {
        const response = await axios.post(
          "http://localhost:5000/login",
          {
            username: this.username,
            password: this.password,
          },
          {
            withCredentials: USE_COOKIES,
          }
        );

        if (!USE_COOKIES) {
          const { access_token, refresh_token } = response.data;
          localStorage.setItem("access_token", access_token);
          localStorage.setItem("refresh_token", refresh_token);
        }

        this.$router.push("/success");
      } catch {
        this.error = "Invalid username or password";
      } finally {
        this.loading = false;
      }
    },
    async signup() {
      if (!this.username || !this.password) {
        this.error = "Both username and password are required.";
        return;
      }
      this.loading = true;
      try {
        const response = await axios.post("http://localhost:5000/register", {
          username: this.username,
          password: this.password,
        });
        if (response.status === 201) {
          this.isSignup = false;
        }
      } catch {
        this.error = "Username already exists or invalid data";
      } finally {
        this.loading = false;
      }
    },
    toggleSignup() {
      this.isSignup = !this.isSignup;
      this.error = "";
    },
    clearTokens() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    },
  },
};
</script>

<style>
.container {
  max-width: 500px;
}
.card {
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}
.btn-link {
  color: #007bff;
}
</style>
