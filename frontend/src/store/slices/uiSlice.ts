import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { RootState } from '../index';

interface UIState {
    sidebarOpen: boolean;
    darkMode: boolean;
    currentModule: 'bakery' | 'tools' | 'academy' | null;
    notifications: Array<{
        id: string;
        type: 'success' | 'error' | 'info' | 'warning';
        message: string;
    }>;
}

const initialState: UIState = {
    sidebarOpen: true,
    darkMode: false,
    currentModule: null,
    notifications: [],
};

const uiSlice = createSlice({
    name: 'ui',
    initialState,
    reducers: {
        toggleSidebar: (state) => {
            state.sidebarOpen = !state.sidebarOpen;
        },
        toggleDarkMode: (state) => {
            state.darkMode = !state.darkMode;
            localStorage.setItem('darkMode', state.darkMode.toString());
        },
        setCurrentModule: (state, action: PayloadAction<'bakery' | 'tools' | 'academy' | null>) => {
            state.currentModule = action.payload;
        },
        addNotification: (state, action: PayloadAction<{
            type: 'success' | 'error' | 'info' | 'warning';
            message: string;
        }>) => {
            const id = new Date().getTime().toString();
            state.notifications.push({
                id,
                ...action.payload,
            });
        },
        removeNotification: (state, action: PayloadAction<string>) => {
            state.notifications = state.notifications.filter(
                (notification) => notification.id !== action.payload
            );
        },
    },
});

export const {
    toggleSidebar,
    toggleDarkMode,
    setCurrentModule,
    addNotification,
    removeNotification,
} = uiSlice.actions;

// Selectors
export const selectUI = (state: RootState) => state.ui;
export const selectSidebarOpen = (state: RootState) => state.ui.sidebarOpen;
export const selectDarkMode = (state: RootState) => state.ui.darkMode;
export const selectCurrentModule = (state: RootState) => state.ui.currentModule;
export const selectNotifications = (state: RootState) => state.ui.notifications;

export default uiSlice.reducer;
