import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server : { 
    proxy: {
      '/query': {
        target: 'http://127.0.0.1:8000/query/',
        changeOrigin: true,
        secure : false,
        rewrite: (path) => path.replace(/^\/query/, '')
      },
      '/list_queries': {
        target: 'http://127.0.0.1:8000/list_queries/',
        changeOrigin: true,
        secure : false,
        rewrite: (path) => path.replace(/^\/list_queries/, '')
      }
    }
  }
})
