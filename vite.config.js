import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  base: './',
  plugins: [react()],
  preview: {
    port: 4173,
    host: '0.0.0.0',
    allowedHosts: ['.onrender.com']
  }
})