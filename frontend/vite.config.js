import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    // Enable access from all network interfaces
    host: "0.0.0.0",
    // Show your network IP in the terminal for easier access
    strictPort: true,
    // Configure proxy for WebSocket and API requests
    proxy: {
      "/ws": {
        target: "ws://localhost:8000",
        ws: true,
        changeOrigin: true,
        // Necessary for secure dev tunnels
        secure: false,
        // Handle redirects properly
        rewrite: (path) => path.replace(/^\/ws/, "/ws"),
      },
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        // Necessary for secure dev tunnels
        secure: false,
        // Handle redirects properly
        rewrite: (path) => path.replace(/^\/api/, "/api"),
      },
    },
  },
});
