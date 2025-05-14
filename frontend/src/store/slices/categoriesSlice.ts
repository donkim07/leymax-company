import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { RootState } from '../index';
import api from '../../utils/api';

import { Category, CategoryUpdateData, CategoryFormData } from '../types';

interface CategoryState {
    items: Category[];
    loading: boolean;
    error: string | null;
}

const initialState: CategoryState = {
    items: [],
    loading: false,
    error: null,
};

// Async thunks
export const fetchCategories = createAsyncThunk(
    'categories/fetchAll',
    async (_, { rejectWithValue }) => {
        try {
            const response = await api.get('/categories');
            return response.data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to fetch categories');
        }
    }
);

export const createCategory = createAsyncThunk(
    'categories/create',
    async (data: CategoryFormData, { rejectWithValue }) => {
        try {
            const response = await api.post('/categories', data);
            return response.data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to create category');
        }
    }
);

export const updateCategory = createAsyncThunk(
    'categories/update',
    async ({ id, ...data }: CategoryUpdateData & { id: number }, { rejectWithValue }) => {
        try {
            const response = await api.put(`/categories/${id}`, data);
            return response.data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to update category');
        }
    }
);

export const deleteCategory = createAsyncThunk(
    'categories/delete',
    async (id: number, { rejectWithValue }) => {
        try {
            await api.delete(`/categories/${id}`);
            return id;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to delete category');
        }
    }
);

const categoriesSlice = createSlice({
    name: 'categories',
    initialState,
    reducers: {
        clearError: (state) => {
            state.error = null;
        },
    },
    extraReducers: (builder) => {
        builder
            // Fetch categories
            .addCase(fetchCategories.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchCategories.fulfilled, (state, action) => {
                state.loading = false;
                state.items = action.payload;
            })
            .addCase(fetchCategories.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            })
            // Create category
            .addCase(createCategory.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(createCategory.fulfilled, (state, action) => {
                state.loading = false;
                state.items.push(action.payload);
            })
            .addCase(createCategory.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            })
            // Update category
            .addCase(updateCategory.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(updateCategory.fulfilled, (state, action) => {
                state.loading = false;
                const index = state.items.findIndex((item) => item.id === action.payload.id);
                if (index !== -1) {
                    state.items[index] = action.payload;
                }
            })
            .addCase(updateCategory.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            })
            // Delete category
            .addCase(deleteCategory.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(deleteCategory.fulfilled, (state, action) => {
                state.loading = false;
                state.items = state.items.filter((item) => item.id !== action.payload);
            })
            .addCase(deleteCategory.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            });
    },
});

export const { clearError } = categoriesSlice.actions;

// Selectors
export const selectCategories = (state: RootState) => state.categories.items;
export const selectCategoriesLoading = (state: RootState) => state.categories.loading;
export const selectCategoriesError = (state: RootState) => state.categories.error;

export default categoriesSlice.reducer;
