from typing import Any, Dict, Optional, Union, List
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            password_hash=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            role=obj_in.role,
            company_id=obj_in.company_id,
            store_id=obj_in.store_id,
            phone=obj_in.phone,
            address=obj_in.address
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["password_hash"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def get_company_users(
        self, db: Session, *, company_id: int, skip: int = 0, limit: int = 100
    ) -> List[User]:
        return (
            db.query(User)
            .filter(User.company_id == company_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_store_users(
        self, db: Session, *, store_id: int, skip: int = 0, limit: int = 100
    ) -> List[User]:
        return (
            db.query(User)
            .filter(User.store_id == store_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

crud_user = CRUDUser(User)
