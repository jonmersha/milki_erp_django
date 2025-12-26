import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  base: "/static/", // REQUIRED for Django
  plugins: [
    react(),
    tailwindcss(), // Tailwind v4 plugin
    VitePWA({
      registerType: "autoUpdate",
      manifest: {
        name: "Milki Systems",
        short_name: "Milki",
        start_url: "/",
        display: "standalone",
        background_color: "#ffffff",
        theme_color: "#0ea5e9",
        icons: [
          {
            src: "icons/icon-192.png",
            sizes: "192x192",
            type: "image/png",
          },
          {
            src: "icons/icon-512.png",
            sizes: "512x512",
            type: "image/png",
          }
        ]
      }
    })
  ],

  build: {
    outDir: "dist",
    emptyOutDir: true,
    assetsDir: "assets",
    manifest: true,
  },
});
