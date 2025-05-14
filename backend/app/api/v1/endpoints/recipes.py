from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud.crud_recipe import crud_recipe
from app.schemas.recipe import Recipe, RecipeCreate, RecipeUpdate, RecipeIngredient, RecipeIngredientCreate

router = APIRouter()

@router.get("/", response_model=List[Recipe])
def read_recipes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """
    Retrieve recipes for the current user's company.
    """
    recipes = crud_recipe.get_multi_by_company(
        db=db, company_id=current_user.company_id, skip=skip, limit=limit
    )
    return recipes

@router.post("/", response_model=Recipe)
def create_recipe(
    *,
    db: Session = Depends(deps.get_db),
    recipe_in: RecipeCreate,
    current_user: Any = Depends(deps.get_current_store_manager)
) -> Any:
    """
    Create new recipe.
    """
    recipe_in.company_id = current_user.company_id
    recipe = crud_recipe.create(db=db, obj_in=recipe_in)
    return recipe

@router.put("/{recipe_id}", response_model=Recipe)
def update_recipe(
    *,
    db: Session = Depends(deps.get_db),
    recipe_id: int,
    recipe_in: RecipeUpdate,
    current_user: Any = Depends(deps.get_current_store_manager)
) -> Any:
    """
    Update a recipe.
    """
    recipe = crud_recipe.get(db=db, id=recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if recipe.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    recipe = crud_recipe.update(db=db, db_obj=recipe, obj_in=recipe_in)
    return recipe

@router.get("/{recipe_id}", response_model=Recipe)
def read_recipe(
    *,
    db: Session = Depends(deps.get_db),
    recipe_id: int,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get recipe by ID.
    """
    recipe = crud_recipe.get(db=db, id=recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if recipe.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return recipe

@router.delete("/{recipe_id}")
def delete_recipe(
    *,
    db: Session = Depends(deps.get_db),
    recipe_id: int,
    current_user: Any = Depends(deps.get_current_store_manager)
) -> Any:
    """
    Delete a recipe.
    """
    recipe = crud_recipe.get(db=db, id=recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if recipe.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    crud_recipe.remove(db=db, id=recipe_id)
    return {"message": "Recipe deleted successfully"} 