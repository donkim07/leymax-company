import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { RootState } from '../index';
import api from '../../utils/api';

interface InventoryItem {
    id: number;
    code: string;
    name: string;
    category: string;
    unitPrice: number;
    quantity: number;
    unit: string;
    reorderPoint: number;
    status: string;
    createdAt: string;
    updatedAt: string;
}

interface InventoryState {
    items: InventoryItem[];
    loading: boolean;
    error: string | null;
    categories: string[];
    units: string[];
}

const initialState: InventoryState = {
    items: [],
    loading: false,
    error: null,
    categories: ['Raw Materials', 'Finished Goods', 'Packaging', 'Tools'],
    units: ['pc', 'kg', 'g', 'l', 'ml'],
};

// Async thunks
export const fetchInventoryItems = createAsyncThunk(
    'inventory/fetchItems',
    async (_, { rejectWithValue }) => {
        try {
            const response = await api.get('/inventory/items');
            return response.data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to fetch inventory items');
        }
    }
);

export const createInventoryItem = createAsyncThunk(
    'inventory/createItem',
    async (itemData: Partial<InventoryItem>, { rejectWithValue }) => {
        try {
            const response = await api.post('/inventory/items', itemData);
            return response.data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to create inventory item');
        }
    }
);

export const updateInventoryItem = createAsyncThunk(
    'inventory/updateItem',
    async ({ id, ...itemData }: Partial<InventoryItem> & { id: number }, { rejectWithValue }) => {
        try {
            const response = await api.put(`/inventory/items/${id}`, itemData);
            return response.data;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to update inventory item');
        }
    }
);

export const deleteInventoryItem = createAsyncThunk(
    'inventory/deleteItem',
    async (id: number, { rejectWithValue }) => {
        try {
            await api.delete(`/inventory/items/${id}`);
            return id;
        } catch (error: any) {
            return rejectWithValue(error.response?.data?.detail || 'Failed to delete inventory item');
        }
    }
);

const inventorySlice = createSlice({
    name: 'inventory',
    initialState,
    reducers: {
        clearError: (state) => {
            state.error = null;
        },
        addCategory: (state, action) => {
            if (!state.categories.includes(action.payload)) {
                state.categories.push(action.payload);
            }
        },
        addUnit: (state, action) => {
            if (!state.units.includes(action.payload)) {
                state.units.push(action.payload);
            }
        },
    },
    extraReducers: (builder) => {
        builder
            // Fetch Items
            .addCase(fetchInventoryItems.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchInventoryItems.fulfilled, (state, action) => {
                state.loading = false;
                state.items = action.payload;
            })
            .addCase(fetchInventoryItems.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            })
            // Create Item
            .addCase(createInventoryItem.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(createInventoryItem.fulfilled, (state, action) => {
                state.loading = false;
                state.items.push(action.payload);
            })
            .addCase(createInventoryItem.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            })
            // Update Item
            .addCase(updateInventoryItem.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(updateInventoryItem.fulfilled, (state, action) => {
                state.loading = false;
                const index = state.items.findIndex((item) => item.id === action.payload.id);
                if (index !== -1) {
                    state.items[index] = action.payload;
                }
            })
            .addCase(updateInventoryItem.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            })
            // Delete Item
            .addCase(deleteInventoryItem.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(deleteInventoryItem.fulfilled, (state, action) => {
                state.loading = false;
                state.items = state.items.filter((item) => item.id !== action.payload);
            })
            .addCase(deleteInventoryItem.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            });
    },
});

export const { clearError, addCategory, addUnit } = inventorySlice.actions;

// Selectors
export const selectInventory = (state: RootState) => state.inventory;
export const selectInventoryItems = (state: RootState) => state.inventory.items;
export const selectInventoryLoading = (state: RootState) => state.inventory.loading;
export const selectInventoryError = (state: RootState) => state.inventory.error;
export const selectCategories = (state: RootState) => state.inventory.categories;
export const selectUnits = (state: RootState) => state.inventory.units;

export default inventorySlice.reducer;
