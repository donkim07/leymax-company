import React from 'react';
import {
    Box,
    TextField,
    MenuItem,
} from '@mui/material';
import { Container, Item } from '../MuiGridFix';
import { Category, CategoryFormData } from '../../store/types';

interface CategoryFormProps {
    formData: CategoryFormData;
    setFormData: React.Dispatch<React.SetStateAction<CategoryFormData>>;
    categories: Category[];
    selectedCategory: Category | null;
}

export const CategoryForm: React.FC<CategoryFormProps> = ({
    formData,
    setFormData,
    categories,
    selectedCategory,
}) => {
    return (
        <Box sx={{ pt: 2 }}>
            <Container spacing={2}>
                <Item xs={12}>
                    <TextField
                        fullWidth
                        label="Category Name"
                        value={formData.name}
                        onChange={(e) => setFormData(prev => ({
                            ...prev,
                            name: e.target.value
                        }))}
                        required
                    />
                </Item>
                <Item xs={12}>
                    <TextField
                        fullWidth
                        label="Description"
                        value={formData.description}
                        onChange={(e) => setFormData(prev => ({
                            ...prev,
                            description: e.target.value
                        }))}
                        multiline
                        rows={3}
                    />
                </Item>
                <Item xs={12}>
                    <TextField
                        select
                        fullWidth
                        label="Parent Category"
                        value={formData.parentId || ''}
                        onChange={(e) => {
                            const value = e.target.value;
                            setFormData(prev => ({
                                ...prev,
                                parentId: value === '' ? null : Number(value)
                            }));
                        }}
                    >
                        <MenuItem value="">
                            <em>None (Top Level)</em>
                        </MenuItem>
                        {categories
                            .filter((cat: Category) => cat.id !== selectedCategory?.id)
                            .map((cat: Category) => (
                                <MenuItem key={cat.id} value={cat.id}>
                                    {cat.name}
                                </MenuItem>
                            ))}
                    </TextField>
                </Item>
            </Container>
        </Box>
    );
};

export default CategoryForm;
