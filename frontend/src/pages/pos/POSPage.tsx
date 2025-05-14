import React, { useState } from 'react';
import {
    Box,
    Paper,
    Typography,
    Card,
    CardContent,
    CardMedia,
    Button,
    Divider,
    List,
    ListItem,
    ListItemText,
    IconButton,
    TextField,
} from '@mui/material';
import {
    Add as AddIcon,
    Remove as RemoveIcon,
    Delete as DeleteIcon,
    Payment as PaymentIcon,
} from '@mui/icons-material';
import { Container, Item } from '../../components/MuiGridFix';

interface CartItem {
    id: number;
    name: string;
    price: number;
    quantity: number;
    image: string;
}

const POSPage: React.FC = () => {
    // Temporary mock data - will be replaced with API data
    const [cartItems, setCartItems] = useState<CartItem[]>([]);
    const [products] = useState([
        {
            id: 1,
            name: 'Chocolate Cake',
            price: 850,
            image: '/images/products/chocolate-cake.jpg',
            category: 'Cakes',
        },
        {
            id: 2,
            name: 'Vanilla Cupcake',
            price: 45,
            image: '/images/products/vanilla-cupcake.jpg',
            category: 'Cupcakes',
        },
        // Add more products here
    ]);

    const addToCart = (product: any) => {
        const existingItem = cartItems.find((item) => item.id === product.id);
        if (existingItem) {
            setCartItems(
                cartItems.map((item) =>
                    item.id === product.id
                        ? { ...item, quantity: item.quantity + 1 }
                        : item
                )
            );
        } else {
            setCartItems([...cartItems, { ...product, quantity: 1 }]);
        }
    };

    const removeFromCart = (productId: number) => {
        const existingItem = cartItems.find((item) => item.id === productId);
        if (existingItem?.quantity === 1) {
            setCartItems(cartItems.filter((item) => item.id !== productId));
        } else {
            setCartItems(
                cartItems.map((item) =>
                    item.id === productId
                        ? { ...item, quantity: item.quantity - 1 }
                        : item
                )
            );
        }
    };

    const deleteFromCart = (productId: number) => {
        setCartItems(cartItems.filter((item) => item.id !== productId));
    };

    const calculateTotal = () => {
        return cartItems.reduce(
            (total, item) => total + item.price * item.quantity,
            0
        );
    };

    return (
        <Box sx={{ height: '100%', display: 'flex' }}>
            {/* Products Grid */}
            <Box sx={{ flex: 1, p: 2, overflowY: 'auto' }}>
                <Container>
                    {products.map((product) => (
                        <Item xs={12} sm={6} md={4} lg={3} key={product.id}>
                            <Card
                                sx={{ cursor: 'pointer' }}
                                onClick={() => addToCart(product)}
                            >
                                <CardMedia
                                    component="img"
                                    height="140"
                                    image={product.image}
                                    alt={product.name}
                                />
                                <CardContent>
                                    <Typography variant="h6" noWrap>
                                        {product.name}
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        ₱{product.price.toFixed(2)}
                                    </Typography>
                                </CardContent>
                            </Card>
                        </Item>
                    ))}
                </Container>
            </Box>

            {/* Cart */}
            <Paper
                sx={{
                    width: 360,
                    display: 'flex',
                    flexDirection: 'column',
                    borderLeft: 1,
                    borderColor: 'divider',
                }}
            >
                <Box sx={{ p: 2 }}>
                    <Typography variant="h6">Current Order</Typography>
                </Box>
                <Divider />

                {/* Cart Items */}
                <List sx={{ flex: 1, overflowY: 'auto' }}>
                    {cartItems.map((item) => (
                        <ListItem
                            key={item.id}
                            secondaryAction={
                                <IconButton
                                    edge="end"
                                    aria-label="delete"
                                    onClick={() => deleteFromCart(item.id)}
                                >
                                    <DeleteIcon />
                                </IconButton>
                            }
                        >
                            <ListItemText
                                primary={item.name}
                                secondary={`₱${item.price.toFixed(2)}`}
                            />
                            <Box sx={{ display: 'flex', alignItems: 'center', ml: 2 }}>
                                <IconButton
                                    size="small"
                                    onClick={() => removeFromCart(item.id)}
                                >
                                    <RemoveIcon />
                                </IconButton>
                                <Typography sx={{ mx: 1 }}>{item.quantity}</Typography>
                                <IconButton
                                    size="small"
                                    onClick={() => addToCart(item)}
                                >
                                    <AddIcon />
                                </IconButton>
                            </Box>
                        </ListItem>
                    ))}
                </List>

                {/* Order Summary */}
                <Box sx={{ p: 2 }}>
                    <Divider sx={{ mb: 2 }} />
                    <Container spacing={2}>
                        <Item xs={12}>
                            <TextField
                                label="Customer Note"
                                fullWidth
                                multiline
                                rows={2}
                                variant="outlined"
                            />
                        </Item>
                        <Item xs={12}>
                            <Typography variant="h6">
                                Total: ₱{calculateTotal().toFixed(2)}
                            </Typography>
                        </Item>
                        <Item xs={12}>
                            <Button
                                variant="contained"
                                fullWidth
                                size="large"
                                startIcon={<PaymentIcon />}
                                disabled={cartItems.length === 0}
                            >
                                Process Payment
                            </Button>
                        </Item>
                    </Container>
                </Box>
            </Paper>
        </Box>
    );
};

export default POSPage;
