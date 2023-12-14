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
      },
      '/plotly_graph': {
        target: 'http://127.0.0.1:8000/plotly_graph/',
        changeOrigin: true,
        secure : false,
        rewrite: (path) => path.replace(/^\/plotly_graph/, '')
      },
      '/list_graphs': {
        target: 'http://127.0.0.1:8000/list_graphs/',
        changeOrigin: true,
        secure : false,
        rewrite: (path) => path.replace(/^\/list_graphs/, '')
      },
      '/add_label': {
        target: 'http://127.0.0.1:8000/add_label/',
        changeOrigin: true,
        secure : false,
        rewrite: (path) => path.replace(/^\/add_label/, '')
      },
      '/list_labels': {
        target: 'http://127.0.0.1:8000/list_labels/',
        changeOrigin: true,
        secure : false,
        rewrite: (path) => path.replace(/^\/list_labels/, '')
      }
    }
  }
})
