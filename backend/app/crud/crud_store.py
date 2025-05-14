from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.company import Store
from app.schemas.company import StoreCreate, StoreUpdate

class CRUDStore(CRUDBase[Store, StoreCreate, StoreUpdate]):
    def get_multi_by_company(
        self, db: Session, *, company_id: int, skip: int = 0, limit: int = 100
    ) -> List[Store]:
        return (
            db.query(Store)
            .filter(Store.company_id == company_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: StoreCreate) -> Store:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Store(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_store = CRUDStore(Store) 