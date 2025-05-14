import React from 'react';
import { useSelector } from 'react-redux';
import {
    Box,
    Drawer,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    IconButton,
    Divider,
    Typography,
    useTheme,
    ListItemButton,
} from '@mui/material';
import {
    Store,
    ShoppingBag,
    School,
    Dashboard,
    Inventory,
    Receipt,
    People,
    Settings,
    ChevronLeft,
} from '@mui/icons-material';
import { selectSidebarOpen, selectCurrentModule } from '../../store/slices/uiSlice';

const Sidebar: React.FC = () => {
    const theme = useTheme();
    const sidebarOpen = useSelector(selectSidebarOpen);
    const currentModule = useSelector(selectCurrentModule);

    const drawerWidth = sidebarOpen ? 280 : 80;

    const mainMenuItems = [
        { icon: <Dashboard />, text: 'Dashboard', path: '/' },
        { icon: <Store />, text: 'POS', path: '/pos' },
        { icon: <Inventory />, text: 'Inventory', path: '/inventory' },
        { icon: <Receipt />, text: 'Orders', path: '/orders' },
        { icon: <People />, text: 'Customers', path: '/customers' },
    ];

    const moduleMenuItems = {
        bakery: [
            { icon: <Store />, text: 'Bakery Shop', path: '/bakery' },
            { icon: <Receipt />, text: 'Production', path: '/bakery/production' },
            { icon: <Inventory />, text: 'Recipes', path: '/bakery/recipes' },
        ],
        tools: [
            { icon: <ShoppingBag />, text: 'Tools Shop', path: '/tools' },
            { icon: <Inventory />, text: 'Suppliers', path: '/tools/suppliers' },
        ],
        academy: [
            { icon: <School />, text: 'Academy', path: '/academy' },
            { icon: <People />, text: 'Students', path: '/academy/students' },
            { icon: <Receipt />, text: 'Courses', path: '/academy/courses' },
        ],
    };

    return (
        <Drawer
            variant="persistent"
            anchor="left"
            open={true}
            sx={{
                width: drawerWidth,
                flexShrink: 0,
                '& .MuiDrawer-paper': {
                    width: drawerWidth,
                    boxSizing: 'border-box',
                    transition: theme.transitions.create(['width'], {
                        easing: theme.transitions.easing.sharp,
                        duration: theme.transitions.duration.enteringScreen,
                    }),
                },
            }}
        >
            <Box sx={{ p: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                {sidebarOpen ? (
                    <Typography variant="h6" noWrap component="div">
                        Leymax POS
                    </Typography>
                ) : null}
                <IconButton>
                    <ChevronLeft />
                </IconButton>
            </Box>
            <Divider />
            
            {/* Main Menu */}
            <List>
                {mainMenuItems.map((item) => (
                    <ListItemButton key={item.text}>
                        <ListItemIcon>{item.icon}</ListItemIcon>
                        {sidebarOpen && <ListItemText primary={item.text} />}
                    </ListItemButton>
                ))}
            </List>
            <Divider />
            
            {/* Module Specific Menu */}
            {currentModule && moduleMenuItems[currentModule] && (
                <>
                    <List>
                        {moduleMenuItems[currentModule].map((item) => (
                            <ListItemButton key={item.text}>
                                <ListItemIcon>{item.icon}</ListItemIcon>
                                {sidebarOpen && <ListItemText primary={item.text} />}
                            </ListItemButton>
                        ))}
                    </List>
                    <Divider />
                </>
            )}
            
            {/* Settings */}
            <List>
                <ListItemButton>
                    <ListItemIcon>
                        <Settings />
                    </ListItemIcon>
                    {sidebarOpen && <ListItemText primary="Settings" />}
                </ListItemButton>
            </List>
        </Drawer>
    );
};

export default Sidebar;
