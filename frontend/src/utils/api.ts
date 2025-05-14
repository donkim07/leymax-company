import axios from 'axios';
import { store } from '../store';

const baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
    baseURL,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true,  // Important for cookies
});

// Add token to requests
api.interceptors.request.use((config) => {
    const token = store.getState().auth.token;
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

// Handle 401 responses
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response?.status === 401) {
            // Clear auth state and redirect to login
            store.dispatch({ type: 'auth/logout' });
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default api;
