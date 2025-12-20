import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
    plugins: [react()],
    base: "/valorant-collections/",
    server: {
        watch: {
            usePolling: true,
        },
        hmr: {
            // This forces the browser to connect back to your WSL IP
            // instead of 'localhost', which can be finicky in WSL2
            host: "localhost",
            protocol: "ws",
        },
    },
});
