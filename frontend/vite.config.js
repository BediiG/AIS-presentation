import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from 'fs'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    https: {
      cert: fs.readFileSync('../frontend-cert.pem'),
      key: fs.readFileSync('../frontend-key.pem'),
    },
    port: 5173,
  },
})
