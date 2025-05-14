from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.company import Company, Store
from app.schemas.company import CompanyCreate, CompanyUpdate, StoreCreate, StoreUpdate

class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Company]:
        return db.query(Company).filter(Company.name == name).first()

    def get_with_stores(self, db: Session, *, id: int) -> Optional[Company]:
        return db.query(Company).filter(Company.id == id).first()

class CRUDStore(CRUDBase[Store, StoreCreate, StoreUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[Store]:
        return db.query(Store).filter(Store.code == code).first()

    def get_company_stores(
        self, db: Session, *, company_id: int, skip: int = 0, limit: int = 100
    ) -> List[Store]:
        return (
            db.query(Store)
            .filter(Store.company_id == company_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_sub_stores(
        self, db: Session, *, parent_store_id: int, skip: int = 0, limit: int = 100
    ) -> List[Store]:
        return (
            db.query(Store)
            .filter(Store.parent_store_id == parent_store_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_main_stores(
        self, db: Session, *, company_id: int, skip: int = 0, limit: int = 100
    ) -> List[Store]:
        return (
            db.query(Store)
            .filter(Store.company_id == company_id)
            .filter(Store.parent_store_id == None)  # noqa
            .offset(skip)
            .limit(limit)
            .all()
        )

crud_company = CRUDCompany(Company)
crud_store = CRUDStore(Store)
