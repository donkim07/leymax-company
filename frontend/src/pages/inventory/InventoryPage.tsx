import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
    Box,
    Button,
    Typography,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    MenuItem,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { Container, Item } from '../../components/MuiGridFix';
import DataTable from '../../components/common/DataTable';
import {
    fetchInventoryItems,
    createInventoryItem,
    selectInventoryItems,
    selectInventoryLoading,
    selectCategories,
    selectUnits,
} from '../../store/slices/inventorySlice';
import type { AppDispatch } from '../../store';

const columns = [
    { id: 'code', label: 'Code', minWidth: 100 },
    { id: 'name', label: 'Name', minWidth: 170 },
    { id: 'category', label: 'Category', minWidth: 130 },
    {
        id: 'unitPrice',
        label: 'Unit Price',
        minWidth: 100,
        align: 'right' as const,
        format: (value: number) => `₱${value.toFixed(2)}`,
    },
    {
        id: 'quantity',
        label: 'Quantity',
        minWidth: 100,
        align: 'right' as const,
    },
    { id: 'unit', label: 'Unit', minWidth: 100 },
    {
        id: 'reorderPoint',
        label: 'Reorder Point',
        minWidth: 130,
        align: 'right' as const,
    },
    { id: 'status', label: 'Status', minWidth: 100 },
];

interface NewItemForm {
    code: string;
    name: string;
    category: string;
    unitPrice: string;
    quantity: string;
    unit: string;
    reorderPoint: string;
}

const initialFormState: NewItemForm = {
    code: '',
    name: '',
    category: '',
    unitPrice: '',
    quantity: '',
    unit: '',
    reorderPoint: '',
};

const getUnitLabel = (unit: string) => {
    const unitLabels: Record<string, string> = {
        pc: 'Piece (pc)',
        kg: 'Kilogram (kg)',
        g: 'Gram (g)',
        l: 'Liter (l)',
        ml: 'Milliliter (ml)',
    };
    return unitLabels[unit] || unit;
};

export default function InventoryPage() {
    const dispatch = useDispatch<AppDispatch>();
    const inventoryItems = useSelector(selectInventoryItems);
    const loading = useSelector(selectInventoryLoading);
    const categories = useSelector(selectCategories);
    const units = useSelector(selectUnits);

    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [formData, setFormData] = useState<NewItemForm>(initialFormState);

    useEffect(() => {
        dispatch(fetchInventoryItems());
    }, [dispatch]);

    const handleInputChange = (field: keyof NewItemForm) => (
        event: React.ChangeEvent<HTMLInputElement>
    ) => {
        setFormData({ ...formData, [field]: event.target.value });
    };

    const handleSubmit = async () => {
        const itemData = {
            ...formData,
            unitPrice: parseFloat(formData.unitPrice),
            quantity: parseInt(formData.quantity),
            reorderPoint: parseInt(formData.reorderPoint),
        };

        const resultAction = await dispatch(createInventoryItem(itemData));
        if (createInventoryItem.fulfilled.match(resultAction)) {
            handleCloseDialog();
        }
    };

    const handleCloseDialog = () => {
        setIsDialogOpen(false);
        setFormData(initialFormState);
    };

    return (
        <Box sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
                <Typography variant="h4">Inventory Management</Typography>
                <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => setIsDialogOpen(true)}
                >
                    Add New Item
                </Button>
            </Box>

            <DataTable
                columns={columns}
                rows={inventoryItems}
                onRowClick={(row) => console.log('Clicked row:', row)}
                defaultSortBy="name"
            />

            <Dialog open={isDialogOpen} onClose={handleCloseDialog} maxWidth="md" fullWidth>
                <DialogTitle>Add New Inventory Item</DialogTitle>
                <DialogContent>
                    <Box component="form" sx={{ mt: 2 }}>
                        <Container spacing={2}>
                            <Item xs={12} sm={6}>
                                <TextField
                                    fullWidth
                                    label="Item Code"
                                    value={formData.code}
                                    onChange={handleInputChange('code')}
                                    required
                                />
                            </Item>
                            <Item xs={12} sm={6}>
                                <TextField
                                    fullWidth
                                    label="Item Name"
                                    value={formData.name}
                                    onChange={handleInputChange('name')}
                                    required
                                />
                            </Item>
                            <Item xs={12} sm={6}>
                                <TextField
                                    select
                                    fullWidth
                                    label="Category"
                                    value={formData.category}
                                    onChange={handleInputChange('category')}
                                    required
                                >
                                    {categories.map((category) => (
                                        <MenuItem key={category} value={category}>
                                            {category}
                                        </MenuItem>
                                    ))}
                                </TextField>
                            </Item>
                            <Item xs={12} sm={6}>
                                <TextField
                                    fullWidth
                                    label="Unit Price"
                                    type="number"
                                    value={formData.unitPrice}
                                    onChange={handleInputChange('unitPrice')}
                                    InputProps={{
                                        startAdornment: <span>₱</span>,
                                    }}
                                    required
                                />
                            </Item>
                            <Item xs={12} sm={6}>
                                <TextField
                                    fullWidth
                                    label="Quantity"
                                    type="number"
                                    value={formData.quantity}
                                    onChange={handleInputChange('quantity')}
                                    required
                                />
                            </Item>
                            <Item xs={12} sm={6}>
                                <TextField
                                    select
                                    fullWidth
                                    label="Unit"
                                    value={formData.unit}
                                    onChange={handleInputChange('unit')}
                                    required
                                >
                                    {units.map((unit) => (
                                        <MenuItem key={unit} value={unit}>
                                            {getUnitLabel(unit)}
                                        </MenuItem>
                                    ))}
                                </TextField>
                            </Item>
                            <Item xs={12} sm={6}>
                                <TextField
                                    fullWidth
                                    label="Reorder Point"
                                    type="number"
                                    value={formData.reorderPoint}
                                    onChange={handleInputChange('reorderPoint')}
                                    required
                                />
                            </Item>
                        </Container>
                    </Box>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseDialog}>Cancel</Button>
                    <Button
                        onClick={handleSubmit}
                        variant="contained"
                        disabled={loading}
                    >
                        {loading ? 'Adding...' : 'Add Item'}
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
}
