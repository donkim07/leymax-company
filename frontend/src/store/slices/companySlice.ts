import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { RootState } from '../index';
import api from '../../utils/api';

interface CompanyState {
    currentCompany: any | null;
    companies: any[];
    stores: any[];
    loading: boolean;
    error: string | null;
}

const initialState: CompanyState = {
    currentCompany: null,
    companies: [],
    stores: [],
    loading: false,
    error: null,
};

// Async thunks
export const fetchCompanies = createAsyncThunk(
    'company/fetchCompanies',
    async (_, { rejectWithValue }) => {
        try {
            const response = await api.get('/companies');
            return response.data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to fetch companies');
        }
    }
);

export const fetchCompanyStores = createAsyncThunk(
    'company/fetchCompanyStores',
    async (companyId: number, { rejectWithValue }) => {
        try {
            const response = await api.get(`/companies/${companyId}/stores`);
            return response.data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to fetch stores');
        }
    }
);

export const setCurrentCompany = createAsyncThunk(
    'company/setCurrentCompany',
    async (companyId: number, { rejectWithValue }) => {
        try {
            const response = await api.get(`/companies/${companyId}`);
            return response.data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to fetch company');
        }
    }
);

const companySlice = createSlice({
    name: 'company',
    initialState,
    reducers: {
        clearCompanyError: (state) => {
            state.error = null;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchCompanies.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchCompanies.fulfilled, (state, action) => {
                state.loading = false;
                state.companies = action.payload;
            })
            .addCase(fetchCompanies.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            })
            .addCase(fetchCompanyStores.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchCompanyStores.fulfilled, (state, action) => {
                state.loading = false;
                state.stores = action.payload;
            })
            .addCase(fetchCompanyStores.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            })
            .addCase(setCurrentCompany.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(setCurrentCompany.fulfilled, (state, action) => {
                state.loading = false;
                state.currentCompany = action.payload;
            })
            .addCase(setCurrentCompany.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            });
    },
});

export const { clearCompanyError } = companySlice.actions;

// Selectors
export const selectCompany = (state: RootState) => state.company;
export const selectCurrentCompany = (state: RootState) => state.company.currentCompany;
export const selectStores = (state: RootState) => state.company.stores;

export default companySlice.reducer;
