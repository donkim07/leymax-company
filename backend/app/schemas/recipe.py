from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class RecipeIngredientBase(BaseModel):
    recipe_id: int
    item_id: int
    quantity: float
    unit: str
    notes: Optional[str] = None

class RecipeIngredientCreate(RecipeIngredientBase):
    pass

class RecipeIngredientUpdate(RecipeIngredientBase):
    pass

class RecipeIngredient(RecipeIngredientBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RecipeBase(BaseModel):
    company_id: int
    name: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    yield_quantity: Optional[float] = None
    yield_unit: Optional[str] = None
    category_id: Optional[int] = None

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    ingredients: List[RecipeIngredient] = []

    class Config:
        from_attributes = True 