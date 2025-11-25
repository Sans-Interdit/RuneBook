import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import mkcert from 'vite-plugin-mkcert';
import path from 'path';
import compression from 'vite-plugin-compression';

export default defineConfig(({ mode }) => {
  // Charger le .env depuis la racine du projet (un niveau au-dessus de frontend)
  const env = loadEnv(mode, path.resolve(__dirname, '..'));

  return {
    envDir: path.resolve(__dirname, '..'),
    server: {
      https: false,
      host: '127.0.0.1',
      port: 5001, // Port pour le dev
    },
    plugins: [
      react(),
      compression({ algorithm: 'brotliCompress' }),
      mkcert(),
    ],
    define: Object.fromEntries(
      Object.entries(env).map(([key, val]) => [key, JSON.stringify(val)])
    ),
  };
});
