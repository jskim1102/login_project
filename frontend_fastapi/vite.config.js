import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // server 객체를 추가합니다.
  server: {
    // 'deep-i.work' 호스트에서의 접속을 허용합니다.
    allowedHosts: ['deep-i.work'],
  }
})