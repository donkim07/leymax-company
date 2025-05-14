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
    Card,
    CardContent,
    CardActions,
    Chip,
    CircularProgress,
    Alert,
    Snackbar,
    MenuItem,
} from '@mui/material';
import {
    Add as AddIcon,
    Edit as EditIcon,
    Delete as DeleteIcon,
} from '@mui/icons-material';
import { Container, Item } from '../../components/MuiGridFix';
import {
    fetchCategories,
    createCategory,
    updateCategory,
    deleteCategory,
    selectCategories,
    selectCategoriesLoading,
    selectCategoriesError,
} from '../../store/slices/categoriesSlice';
import { Category, CategoryFormData } from '../../store/types';
import { AppDispatch } from '../../store';

interface CategoryWithChildren extends Category {
    children: CategoryWithChildren[];
}

const initialFormState: CategoryFormData = {
    name: '',
    description: '',
    parentId: null,
};

const buildCategoryTree = (categories: Category[]): CategoryWithChildren[] => {
    const categoryMap = new Map<number, CategoryWithChildren>();
    const roots: CategoryWithChildren[] = [];

    // First pass: Create all category nodes
    categories.forEach(cat => {
        categoryMap.set(cat.id, { ...cat, children: [] } as CategoryWithChildren);
    });

    // Second pass: Build the tree structure
    categories.forEach(cat => {
        const node = categoryMap.get(cat.id)!;
        if (!cat.parentId) {
            roots.push(node);
        } else {
            const parent = categoryMap.get(cat.parentId);
            if (parent) {
                parent.children.push(node);
            } else {
                roots.push(node);
            }
        }
    });

    return roots;
};

const CategoryCard: React.FC<{
    category: CategoryWithChildren;
    level?: number;
    onEdit: (category: Category) => void;
    onDelete: (id: number) => void;
}> = ({ category, level = 0, onEdit, onDelete }) => {
    return (
        <>
            <Item xs={12} sm={6} md={4}>
                <Box sx={{ ml: level * 2 }}>
                    <Card>
                        <CardContent>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                <Box>
                                    <Typography variant="h6" component="div">
                                        {category.name}
                                    </Typography>
                                    {category.parentId && (
                                        <Typography variant="caption" color="text.secondary">
                                            Sub-category
                                        </Typography>
                                    )}
                                </Box>
                                <Chip
                                    label={`${category.itemCount || 0} items`}
                                    size="small"
                                    color="primary"
                                />
                            </Box>
                            <Typography
                                variant="body2"
                                color="text.secondary"
                                sx={{ minHeight: '40px', mb: 1 }}
                            >
                                {category.description}
                            </Typography>
                        </CardContent>
                        <CardActions>
                            <Button
                                size="small"
                                startIcon={<EditIcon />}
                                onClick={() => onEdit(category)}
                            >
                                Edit
                            </Button>
                            <Button
                                size="small"
                                color="error"
                                startIcon={<DeleteIcon />}
                                onClick={() => onDelete(category.id)}
                            >
                                Delete
                            </Button>
                        </CardActions>
                    </Card>
                </Box>
            </Item>
            {category.children.map(child => (
                <CategoryCard
                    key={child.id}
                    category={child}
                    level={level + 1}
                    onEdit={onEdit}
                    onDelete={onDelete}
                />
            ))}
        </>
    );
};

export default function CategoriesPage() {
    const dispatch = useDispatch<AppDispatch>();
    const categories = useSelector(selectCategories);
    const loading = useSelector(selectCategoriesLoading);
    const error = useSelector(selectCategoriesError);

    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
    const [categoryToDelete, setCategoryToDelete] = useState<number | null>(null);
    const [selectedCategory, setSelectedCategory] = useState<Category | null>(null);
    const [formData, setFormData] = useState<CategoryFormData>(initialFormState);
    const [snackbar, setSnackbar] = useState<{
        open: boolean;
        message: string;
        severity: 'success' | 'error';
    }>({
        open: false,
        message: '',
        severity: 'success',
    });

    useEffect(() => {
        void dispatch(fetchCategories());
    }, [dispatch]);

    const handleOpenDialog = (category?: Category) => {
        if (category) {
            setSelectedCategory(category);
            setFormData({
                name: category.name,
                description: category.description,
                parentId: category.parentId,
            });
        } else {
            setSelectedCategory(null);
            setFormData(initialFormState);
        }
        setIsDialogOpen(true);
    };

    const handleCloseDialog = () => {
        setIsDialogOpen(false);
        setSelectedCategory(null);
        setFormData(initialFormState);
    };

    const handleSubmit = async () => {
        try {
            if (selectedCategory) {
                await dispatch(updateCategory({
                    id: selectedCategory.id,
                    ...formData
                })).unwrap();
                setSnackbar({
                    open: true,
                    message: 'Category updated successfully',
                    severity: 'success',
                });
            } else {
                await dispatch(createCategory(formData)).unwrap();
                setSnackbar({
                    open: true,
                    message: 'Category created successfully',
                    severity: 'success',
                });
            }
            handleCloseDialog();
        } catch (error) {
            setSnackbar({
                open: true,
                message: 'Failed to save category',
                severity: 'error',
            });
        }
    };

    const handleDeleteClick = (categoryId: number) => {
        setCategoryToDelete(categoryId);
        setDeleteConfirmOpen(true);
    };

    const handleConfirmDelete = async () => {
        if (categoryToDelete) {
            try {
                await dispatch(deleteCategory(categoryToDelete)).unwrap();
                setSnackbar({
                    open: true,
                    message: 'Category deleted successfully',
                    severity: 'success',
                });
            } catch (error) {
                setSnackbar({
                    open: true,
                    message: 'Failed to delete category',
                    severity: 'error',
                });
            }
        }
        setDeleteConfirmOpen(false);
        setCategoryToDelete(null);
    };

    const handleCancelDelete = () => {
        setDeleteConfirmOpen(false);
        setCategoryToDelete(null);
    };

    const handleCloseSnackbar = () => {
        setSnackbar(prev => ({
            ...prev,
            open: false,
        }));
    };

    const categoryTree = buildCategoryTree(categories);

    return (
        <Box sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
                <Typography variant="h4">Categories</Typography>
                <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => handleOpenDialog()}
                >
                    Add Category
                </Button>
            </Box>

            {error && (
                <Alert severity="error" sx={{ mb: 3 }}>
                    {error}
                </Alert>
            )}

            <Container spacing={3}>
                {categoryTree.map((category) => (
                    <CategoryCard
                        key={category.id}
                        category={category}
                        onEdit={handleOpenDialog}
                        onDelete={handleDeleteClick}
                    />
                ))}
            </Container>

            <Dialog open={isDialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
                <DialogTitle>
                    {selectedCategory ? 'Edit Category' : 'Add New Category'}
                </DialogTitle>
                <DialogContent>
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
                                        .filter(cat => cat.id !== selectedCategory?.id)
                                        .map((cat) => (
                                            <MenuItem key={cat.id} value={cat.id}>
                                                {cat.name}
                                            </MenuItem>
                                        ))}
                                </TextField>
                            </Item>
                        </Container>
                    </Box>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseDialog}>Cancel</Button>
                    <Button
                        onClick={handleSubmit}
                        variant="contained"
                        disabled={!formData.name}
                    >
                        {selectedCategory ? 'Save Changes' : 'Add Category'}
                    </Button>
                </DialogActions>
            </Dialog>

            <Dialog
                open={deleteConfirmOpen}
                onClose={handleCancelDelete}
                aria-labelledby="delete-dialog-title"
                aria-describedby="delete-dialog-description"
            >
                <DialogTitle id="delete-dialog-title">
                    Confirm Delete
                </DialogTitle>
                <DialogContent>
                    <Typography variant="body1" id="delete-dialog-description">
                        Are you sure you want to delete this category? This action cannot be undone.
                        Any items in this category will need to be reassigned.
                    </Typography>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCancelDelete}>
                        Cancel
                    </Button>
                    <Button onClick={handleConfirmDelete} color="error" autoFocus>
                        Delete
                    </Button>
                </DialogActions>
            </Dialog>

            <Snackbar
                open={snackbar.open}
                autoHideDuration={6000}
                onClose={handleCloseSnackbar}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            >
                <Alert
                    onClose={handleCloseSnackbar}
                    severity={snackbar.severity}
                    sx={{ width: '100%' }}
                >
                    {snackbar.message}
                </Alert>
            </Snackbar>
        </Box>
    );
}
