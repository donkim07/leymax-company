import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import {
    Container,
    Box,
    Typography,
    TextField,
    Button,
    Paper,
    Link,
    Alert,
    Grid as MuiGrid,
    MenuItem,
    Divider,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { register, selectAuthError, selectAuthLoading } from '../../store/slices/authSlice';
import { AppDispatch } from '../../store';

// Styled components to fix TypeScript issues with Grid
const Grid = styled(MuiGrid)({});

// Company types from backend
enum CompanyType {
    BAKERY = "bakery",
    TOOLS = "tools",
    ACADEMY = "academy"
}

interface CompanyData {
    name: string;
    type: CompanyType;
    description: string;
    address: string;
    phone: string;
    email: string;
}

interface StoreData {
    name: string;
    type: 'main';
    address: string;
    phone: string;
    email: string;
}

interface FormData {
    email: string;
    password: string;
    first_name: string;
    last_name: string;
    phone: string;
    company: CompanyData;
    main_store: StoreData;
}

const RegisterPage: React.FC = () => {
    const dispatch = useDispatch<AppDispatch>();
    const navigate = useNavigate();
    const error = useSelector(selectAuthError);
    const loading = useSelector(selectAuthLoading);

    const [formData, setFormData] = useState<FormData>({
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        phone: '',
        company: {
            name: '',
            type: CompanyType.BAKERY,
            description: '',
            address: '',
            phone: '',
            email: '',
        },
        main_store: {
            name: '',
            type: 'main',
            address: '',
            phone: '',
            email: '',
        }
    });

    const handleChange = (section: 'root' | 'company' | 'main_store', field: string) => 
        (e: React.ChangeEvent<HTMLInputElement>) => {
            if (section === 'root') {
                setFormData({ ...formData, [field]: e.target.value });
            } else {
                setFormData({
                    ...formData,
                    [section]: {
                        ...formData[section],
                        [field]: e.target.value
                    }
                });
            }
        };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const result = await dispatch(register(formData));
        if (register.fulfilled.match(result)) {
            navigate('/login');
        }
    };

    return (
        <Container component="main" maxWidth="md">
            <Box
                sx={{
                    marginTop: 8,
                    marginBottom: 8,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}
            >
                <Paper
                    elevation={3}
                    sx={{
                        padding: 4,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        width: '100%',
                    }}
                >
                    <Typography component="h1" variant="h5" gutterBottom>
                        Create Account
                    </Typography>
                    {error && (
                        <Alert severity="error" sx={{ mt: 2, width: '100%' }}>
                            {error}
                        </Alert>
                    )}
                    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3, width: '100%' }}>
                        <Typography variant="h6" gutterBottom>
                            Personal Information
                        </Typography>
                        <Grid container spacing={2}>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    required
                                    fullWidth
                                    label="First Name"
                                    name="first_name"
                                    value={formData.first_name}
                                    onChange={handleChange('root', 'first_name')}
                                />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    required
                                    fullWidth
                                    label="Last Name"
                                    name="last_name"
                                    value={formData.last_name}
                                    onChange={handleChange('root', 'last_name')}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    required
                                    fullWidth
                                    label="Email Address"
                                    name="email"
                                    type="email"
                                    value={formData.email}
                                    onChange={handleChange('root', 'email')}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    required
                                    fullWidth
                                    label="Password"
                                    name="password"
                                    type="password"
                                    value={formData.password}
                                    onChange={handleChange('root', 'password')}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    fullWidth
                                    label="Phone"
                                    name="phone"
                                    value={formData.phone}
                                    onChange={handleChange('root', 'phone')}
                                />
                            </Grid>
                        </Grid>

                        <Divider sx={{ my: 3 }} />

                        <Typography variant="h6" gutterBottom>
                            Company Information
                        </Typography>
                        <Grid container spacing={2}>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    required
                                    fullWidth
                                    label="Company Name"
                                    name="company.name"
                                    value={formData.company.name}
                                    onChange={handleChange('company', 'name')}
                                />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    required
                                    select
                                    fullWidth
                                    label="Company Type"
                                    name="company.type"
                                    value={formData.company.type}
                                    onChange={handleChange('company', 'type')}
                                >
                                    {Object.entries(CompanyType).map(([key, value]) => (
                                        <MenuItem key={value} value={value}>
                                            {key.charAt(0) + key.slice(1).toLowerCase()}
                                        </MenuItem>
                                    ))}
                                </TextField>
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    fullWidth
                                    label="Company Description"
                                    name="company.description"
                                    multiline
                                    rows={2}
                                    value={formData.company.description}
                                    onChange={handleChange('company', 'description')}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    fullWidth
                                    label="Company Address"
                                    name="company.address"
                                    value={formData.company.address}
                                    onChange={handleChange('company', 'address')}
                                />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    fullWidth
                                    label="Company Phone"
                                    name="company.phone"
                                    value={formData.company.phone}
                                    onChange={handleChange('company', 'phone')}
                                />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    fullWidth
                                    label="Company Email"
                                    name="company.email"
                                    type="email"
                                    value={formData.company.email}
                                    onChange={handleChange('company', 'email')}
                                />
                            </Grid>
                        </Grid>

                        <Divider sx={{ my: 3 }} />

                        <Typography variant="h6" gutterBottom>
                            Main Store Information
                        </Typography>
                        <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <TextField
                                    required
                                    fullWidth
                                    label="Store Name"
                                    name="main_store.name"
                                    value={formData.main_store.name}
                                    onChange={handleChange('main_store', 'name')}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    fullWidth
                                    label="Store Address"
                                    name="main_store.address"
                                    value={formData.main_store.address}
                                    onChange={handleChange('main_store', 'address')}
                                />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    fullWidth
                                    label="Store Phone"
                                    name="main_store.phone"
                                    value={formData.main_store.phone}
                                    onChange={handleChange('main_store', 'phone')}
                                />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    fullWidth
                                    label="Store Email"
                                    name="main_store.email"
                                    type="email"
                                    value={formData.main_store.email}
                                    onChange={handleChange('main_store', 'email')}
                                />
                            </Grid>
                        </Grid>

                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                            disabled={loading}
                        >
                            {loading ? 'Creating Account...' : 'Create Account'}
                        </Button>
                        <Box sx={{ textAlign: 'center' }}>
                            <Link href="/login" variant="body2">
                                {"Already have an account? Sign In"}
                            </Link>
                        </Box>
                    </Box>
                </Paper>
            </Box>
        </Container>
    );
};

export default RegisterPage;
