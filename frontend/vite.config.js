import fs from "node:fs";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],

  server: {
    host: "127.0.0.1",
    port: 443,

    https: {
      key: fs.readFileSync("./certs/www.smca.com-key.pem"),
      cert: fs.readFileSync("./certs/www.smca.com.pem"),
    },

    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
});