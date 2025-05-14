import React from 'react';
import { Box, Container, useTheme } from '@mui/material';
import { useSelector } from 'react-redux';
import { selectSidebarOpen } from '../../store/slices/uiSlice';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import NotificationSystem from './NotificationSystem';

interface MainLayoutProps {
    children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
    const theme = useTheme();
    const sidebarOpen = useSelector(selectSidebarOpen);

    return (
        <Box sx={{ display: 'flex', minHeight: '100vh' }}>
            <Sidebar />
            <Box
                component="main"
                sx={{
                    flexGrow: 1,
                    transition: theme.transitions.create('margin', {
                        easing: theme.transitions.easing.sharp,
                        duration: theme.transitions.duration.leavingScreen,
                    }),
                    marginLeft: sidebarOpen ? '280px' : '80px',
                    bgcolor: theme.palette.background.default,
                }}
            >
                <Navbar />
                <Container maxWidth="xl" sx={{ mt: 2, mb: 4 }}>
                    {children}
                </Container>
                <NotificationSystem />
            </Box>
        </Box>
    );
};

export default MainLayout;
