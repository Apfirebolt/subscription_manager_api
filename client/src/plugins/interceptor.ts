import axios, { type InternalAxiosRequestConfig, type AxiosResponse, type AxiosError } from 'axios';
import Cookie from 'js-cookie';

const baseURL: string = 'http://localhost:8000/api/';

const httpClient = axios.create({ baseURL });

// Request Interceptor
httpClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const userCookie = Cookie.get('user');
    if (userCookie) {
      const authData = JSON.parse(userCookie);
      if (authData.token) {
        config.headers.Authorization = `Bearer ${authData.token}`;
      }
    }
    return config;
  },
  (error: AxiosError) => Promise.reject(error)
);

// Response Interceptor
httpClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

export default httpClient;