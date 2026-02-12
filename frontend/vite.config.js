import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';


export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // ДОБАВИТЬ: слушать все интерфейсы внутри контейнера
    port: 5173,
    watch: {
      usePolling: true,
    },
  },
});
