import React from 'react';
import {
    Box,
    Paper,
    Typography,
    Card,
    CardContent,
    CardHeader,
    IconButton,
} from '@mui/material';
import {
    MoreVert as MoreVertIcon,
    TrendingUp,
    Store,
    ShoppingCart,
    Group,
} from '@mui/icons-material';
import { Container, Item } from '../components/MuiGridFix';

const DashboardPage: React.FC = () => {
    // Temporary mock data - will be replaced with real data from API
    const stats = [
        {
            title: 'Total Sales',
            value: '₱85,420',
            icon: <TrendingUp />,
            change: '+15%',
            period: 'vs last month',
        },
        {
            title: 'Active Orders',
            value: '24',
            icon: <ShoppingCart />,
            change: '+3',
            period: 'since yesterday',
        },
        {
            title: 'Store Traffic',
            value: '156',
            icon: <Store />,
            change: '+8%',
            period: 'vs last week',
        },
        {
            title: 'New Customers',
            value: '12',
            icon: <Group />,
            change: '+2',
            period: 'today',
        },
    ];

    return (
        <Box sx={{ py: 3 }}>
            <Typography variant="h4" sx={{ mb: 4 }}>
                Dashboard
            </Typography>

            {/* Stats Cards */}
            <Container spacing={3} sx={{ mb: 4 }}>
                {stats.map((stat) => (
                    <Item key={stat.title} xs={12} sm={6} md={3}>
                        <Paper
                            sx={{
                                p: 2,
                                display: 'flex',
                                flexDirection: 'column',
                                height: '100%',
                            }}
                        >
                            <Box
                                sx={{
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'space-between',
                                    mb: 2,
                                }}
                            >
                                <Box
                                    sx={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        color: 'primary.main',
                                    }}
                                >
                                    {stat.icon}
                                </Box>
                                <Typography
                                    variant="caption"
                                    color="success.main"
                                    sx={{ display: 'flex', alignItems: 'center' }}
                                >
                                    {stat.change}
                                </Typography>
                            </Box>
                            <Typography variant="h4" component="div">
                                {stat.value}
                            </Typography>
                            <Typography color="text.secondary" sx={{ mb: 1 }}>
                                {stat.title}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                                {stat.period}
                            </Typography>
                        </Paper>
                    </Item>
                ))}
            </Container>

            {/* Recent Activity */}
            <Container spacing={3}>
                <Item xs={12} md={8}>
                    <Card>
                        <CardHeader
                            title="Recent Orders"
                            action={
                                <IconButton aria-label="settings">
                                    <MoreVertIcon />
                                </IconButton>
                            }
                        />
                        <CardContent>
                            <Typography color="text.secondary">
                                No recent orders to display.
                            </Typography>
                        </CardContent>
                    </Card>
                </Item>
                <Item xs={12} md={4}>
                    <Card>
                        <CardHeader
                            title="Low Stock Items"
                            action={
                                <IconButton aria-label="settings">
                                    <MoreVertIcon />
                                </IconButton>
                            }
                        />
                        <CardContent>
                            <Typography color="text.secondary">
                                No low stock items to display.
                            </Typography>
                        </CardContent>
                    </Card>
                </Item>
            </Container>
        </Box>
    );
};

export default DashboardPage;
