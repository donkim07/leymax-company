export interface Category {
    id: number;
    name: string;
    description: string;
    parentId: number | null;
    itemCount?: number;
    createdAt?: string;
    updatedAt?: string;
}

export interface CategoryUpdateData {
    name: string;
    description: string;
    parentId: number | null;
}

export interface CategoryFormData {
    name: string;
    description: string;
    parentId: number | null;
}
