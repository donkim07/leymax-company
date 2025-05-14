import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { RootState } from '../index';
import api from '../../utils/api';

interface AuthState {
    token: string | null;
    user: any | null;
    isAuthenticated: boolean;
    loading: boolean;
    error: string | null;
}

const initialState: AuthState = {
    token: localStorage.getItem('token'),
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null,
};

// Helper function to format error messages
const formatError = (error: any): string => {
    if (typeof error === 'string') return error;
    if (error?.response?.data?.detail) {
        const detail = error.response.data.detail;
        if (Array.isArray(detail)) {
            // Handle validation errors array
            return detail.map(err => {
                if (typeof err === 'object' && err.msg) {
                    return err.msg;
                }
                return String(err);
            }).join(', ');
        }
        return String(detail);
    }
    return 'An unexpected error occurred';
};

// Async thunks
export const register = createAsyncThunk(
    'auth/register',
    async (userData: { 
        email: string; 
        password: string;
        first_name: string;
        last_name: string;
        role?: string;
    }, { rejectWithValue }) => {
        try {
            const response = await api.post('/auth/register', userData);
            return response.data;
        } catch (error: any) {
            return rejectWithValue(formatError(error));
        }
    }
);

export const login = createAsyncThunk(
    'auth/login',
    async (credentials: { email: string; password: string }, { rejectWithValue }) => {
        try {
            const formData = new URLSearchParams();
            formData.append('username', credentials.email);
            formData.append('password', credentials.password);

            const response = await api.post('/auth/login', formData, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                withCredentials: true  // Important for cookies
            });

            const { user, token } = response.data;
            
            // Store token
            localStorage.setItem('token', token.access_token);

            return {
                token: token.access_token,
                user: user,
            };
        } catch (error: any) {
            return rejectWithValue(formatError(error));
        }
    }
);

export const getCurrentUser = createAsyncThunk(
    'auth/getCurrentUser',
    async (_, { rejectWithValue }) => {
        try {
            const response = await api.get('/users/me', {
                withCredentials: true  // Important for cookies
            });
            return response.data;
        } catch (error: any) {
            return rejectWithValue(formatError(error));
        }
    }
);

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        logout: (state) => {
            localStorage.removeItem('token');
            state.token = null;
            state.user = null;
            state.isAuthenticated = false;
        },
        clearError: (state) => {
            state.error = null;
        },
    },
    extraReducers: (builder) => {
        builder
            // Register cases
            .addCase(register.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(register.fulfilled, (state, action) => {
                state.loading = false;
                state.user = action.payload;
            })
            .addCase(register.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            })
            // Login cases
            .addCase(login.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(login.fulfilled, (state, action) => {
                state.loading = false;
                state.token = action.payload.token;
                state.user = action.payload.user;
                state.isAuthenticated = true;
            })
            .addCase(login.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            })
            .addCase(getCurrentUser.pending, (state) => {
                state.loading = true;
            })
            .addCase(getCurrentUser.fulfilled, (state, action) => {
                state.loading = false;
                state.user = action.payload;
                state.isAuthenticated = true;
            })
            .addCase(getCurrentUser.rejected, (state) => {
                state.loading = false;
                state.token = null;
                state.user = null;
                state.isAuthenticated = false;
            });
    },
});

export const { logout, clearError } = authSlice.actions;

// Selectors
export const selectAuth = (state: RootState) => state.auth;
export const selectUser = (state: RootState) => state.auth.user;
export const selectIsAuthenticated = (state: RootState) => state.auth.isAuthenticated;
export const selectToken = (state: RootState) => state.auth.token;
export const selectAuthLoading = (state: RootState) => state.auth.loading;
export const selectAuthError = (state: RootState) => state.auth.error;

export default authSlice.reducer;
