from typing import List, Optional, Any, Dict, Union
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.company import Company, Store, CompanyType, StoreType
from app.schemas.register import CompanyCreate, StoreCreate

class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyCreate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Company]:
        return db.query(Company).filter(Company.name == name).first()
    
    def create_with_store(
        self, 
        db: Session, 
        *, 
        company_in: CompanyCreate,
        store_in: StoreCreate
    ) -> Company:
        # Create company
        db_company = Company(
            name=company_in.name,
            type=company_in.type,
            description=company_in.description,
            address=company_in.address,
            phone=company_in.phone,
            email=company_in.email,
            logo_url=company_in.logo_url
        )
        db.add(db_company)
        db.flush()  # Get company ID without committing
        
        # Create main store
        db_store = Store(
            company_id=db_company.id,
            name=store_in.name,
            type=store_in.type,
            address=store_in.address,
            phone=store_in.phone,
            email=store_in.email
        )
        db.add(db_store)
        db.commit()
        db.refresh(db_company)
        return db_company
    
    def create_store(
        self,
        db: Session,
        *,
        company_id: int,
        store_in: StoreCreate,
        parent_store_id: Optional[int] = None
    ) -> Store:
        db_store = Store(
            company_id=company_id,
            parent_store_id=parent_store_id,
            name=store_in.name,
            type=store_in.type,
            address=store_in.address,
            phone=store_in.phone,
            email=store_in.email
        )
        db.add(db_store)
        db.commit()
        db.refresh(db_store)
        return db_store
    
    def get_company_stores(
        self, db: Session, *, company_id: int
    ) -> List[Store]:
        return db.query(Store).filter(Store.company_id == company_id).all()

crud_company = CRUDCompany(Company)
