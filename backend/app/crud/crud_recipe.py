from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeUpdate

class CRUDRecipe(CRUDBase[Recipe, RecipeCreate, RecipeUpdate]):
    def get_multi_by_company(
        self, db: Session, *, company_id: int, skip: int = 0, limit: int = 100
    ) -> List[Recipe]:
        return (
            db.query(Recipe)
            .filter(Recipe.company_id == company_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: RecipeCreate) -> Recipe:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Recipe(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_recipe = CRUDRecipe(Recipe) 