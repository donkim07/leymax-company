import React from 'react';
import {
    AppBar,
    Toolbar,
    IconButton,
    Typography,
    Button,
    Avatar,
    Menu,
    MenuItem,
    Divider,
    Box,
    useTheme,
} from '@mui/material';
import {
    Menu as MenuIcon,
    Brightness4,
    Brightness7,
    Store,
    CorporateFare,
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { toggleSidebar, toggleDarkMode } from '../../store/slices/uiSlice';
import { logout, selectUser } from '../../store/slices/authSlice';
import { selectCurrentCompany } from '../../store/slices/companySlice';
import CompanySelector from '../CompanySelector';

const Navbar: React.FC = () => {
    const theme = useTheme();
    const dispatch = useDispatch();
    const user = useSelector(selectUser);
    const currentCompany = useSelector(selectCurrentCompany);
    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

    const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleLogout = () => {
        dispatch(logout());
        handleClose();
    };

    return (
        <AppBar
            position="sticky"
            elevation={0}
            sx={{
                bgcolor: theme.palette.background.paper,
                borderBottom: `1px solid ${theme.palette.divider}`,
            }}
        >
            <Toolbar>
                <IconButton
                    edge="start"
                    color="inherit"
                    aria-label="menu"
                    onClick={() => dispatch(toggleSidebar())}
                >
                    <MenuIcon />
                </IconButton>

                <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center', gap: 2 }}>
                    {currentCompany && (
                        <>
                            <CompanySelector />
                            <Divider orientation="vertical" flexItem />
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                <Store />
                                <Typography variant="subtitle1">Main Store</Typography>
                            </Box>
                        </>
                    )}
                </Box>

                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <IconButton color="inherit" onClick={() => dispatch(toggleDarkMode())}>
                        {theme.palette.mode === 'dark' ? <Brightness7 /> : <Brightness4 />}
                    </IconButton>

                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Avatar
                            alt={user?.first_name}
                            src={user?.avatar_url}
                            sx={{ width: 40, height: 40, cursor: 'pointer' }}
                            onClick={handleMenu}
                        />
                        <Box>
                            <Typography variant="subtitle1">
                                {user?.first_name} {user?.last_name}
                            </Typography>
                            <Typography variant="caption" color="textSecondary">
                                {user?.role}
                            </Typography>
                        </Box>
                    </Box>
                </Box>

                <Menu
                    id="menu-appbar"
                    anchorEl={anchorEl}
                    anchorOrigin={{
                        vertical: 'bottom',
                        horizontal: 'right',
                    }}
                    keepMounted
                    transformOrigin={{
                        vertical: 'top',
                        horizontal: 'right',
                    }}
                    open={Boolean(anchorEl)}
                    onClose={handleClose}
                >
                    <MenuItem onClick={handleClose}>Profile</MenuItem>
                    <MenuItem onClick={handleClose}>Settings</MenuItem>
                    <Divider />
                    <MenuItem onClick={handleLogout}>Logout</MenuItem>
                </Menu>
            </Toolbar>
        </AppBar>
    );
};

export default Navbar;
