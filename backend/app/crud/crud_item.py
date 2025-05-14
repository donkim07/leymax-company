from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.crud.base import CRUDBase
from app.models.item import Item, Category
from app.schemas.item import ItemCreate, ItemUpdate, CategoryCreate, CategoryUpdate

class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def get_by_barcode(self, db: Session, *, barcode: str) -> Optional[Item]:
        return db.query(Item).filter(Item.barcode == barcode).first()

    def get_company_items(
        self, db: Session, *, company_id: int, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        return (
            db.query(Item)
            .filter(Item.company_id == company_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_category_items(
        self, db: Session, *, category_id: int, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        return (
            db.query(Item)
            .filter(Item.category_id == category_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_name(
        self, db: Session, *, name: str, company_id: int
    ) -> Optional[Item]:
        return db.query(Item).filter(
            and_(Item.name == name, Item.company_id == company_id)
        ).first()

class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def get_by_name(
        self, db: Session, *, name: str, company_id: int
    ) -> Optional[Category]:
        return db.query(Category).filter(
            and_(Category.name == name, Category.company_id == company_id)
        ).first()

    def get_company_categories(
        self, db: Session, *, company_id: int, skip: int = 0, limit: int = 100
    ) -> List[Category]:
        return (
            db.query(Category)
            .filter(Category.company_id == company_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_subcategories(
        self, db: Session, *, parent_id: int, skip: int = 0, limit: int = 100
    ) -> List[Category]:
        return (
            db.query(Category)
            .filter(Category.parent_id == parent_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

crud_item = CRUDItem(Item)
crud_category = CRUDCategory(Category)
