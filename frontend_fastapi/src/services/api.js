// src/services/api.js
import axios from 'axios';
import useAuthStore from '../store/authStore';

const apiClient = axios.create({
  // .env 파일의 변수를 읽어와 baseURL로 사용
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

apiClient.interceptors.request.use((config) => {
  // 로컬 스토리지를 직접 읽는 대신, 항상 Zustand 스토어의 최신 상태를 가져옵니다.
  const { token } = useAuthStore.getState();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // 자동 로그아웃 처리
      useAuthStore.getState().logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// 회원가입
export const signupUser = (userData) => {
  return apiClient.post('/users/', userData);
};

// 로그인
export const loginUser = (loginData) => {
  // FastAPI OAuth2PasswordRequestForm 형식에 맞게 변환
  const formData = new FormData();
  formData.append('username', loginData.email);
  formData.append('password', loginData.password);
  
  return apiClient.post('/token', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
};

export const api = {
  signupUser: (userData) => {
    return apiClient.post('/users/', userData);
  },

  loginUser: (loginData) => {
    const formData = new FormData();
    formData.append('username', loginData.email);
    formData.append('password', loginData.password);
    
    return apiClient.post('/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  },

  // 구글 로그인 (새로 추가)
  loginWithGoogle: (googleToken) => {
    // 백엔드로 구글 id_token을 전송합니다.
    return apiClient.post('/auth/google', { token: googleToken });
  }
};