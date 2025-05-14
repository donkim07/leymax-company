import logging
import pymysql
from sqlalchemy import create_engine, text
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.models.user import UserRole
from app.models.company import CompanyType, StoreType, Company, Store
from app.crud.crud_user import crud_user
from app.schemas.user import UserCreate
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db() -> None:
    # Try to create database if it doesn't exist
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",
        )
        cursor = conn.cursor()
        
        # Drop database if exists and recreate
        cursor.execute("DROP DATABASE IF EXISTS leymax_webpos")
        cursor.execute("CREATE DATABASE leymax_webpos")
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("Database leymax_webpos recreated")
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        return

    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully")

        # Create initial data
        db = SessionLocal()
        
        # Create default company if it doesn't exist
        company = Company(
            name="Default Company",
            type=CompanyType.BAKERY,
            description="Default company for testing",
            email="company@example.com",
            phone="1234567890",
            tax_number="TAX123",
            registration_number="REG123"
        )
        db.add(company)
        db.commit()
        db.refresh(company)
        logger.info(f"Default company created: {company.name}")
        
        # Create default store
        store = Store(
            company_id=company.id,
            name="Main Store",
            type=StoreType.MAIN,
            email="store@example.com",
            phone="1234567890"
        )
        db.add(store)
        db.commit()
        db.refresh(store)
        logger.info(f"Default store created: {store.name}")

        # Create a test admin user
        user_in = UserCreate(
            email="admin@example.com",
            password="password123",
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN,
            company_id=company.id,
            store_id=store.id
        )
        user = crud_user.create(db=db, obj_in=user_in)
        logger.info(f"Admin user created: {user.email}")
        
        db.close()
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise  # Re-raise the exception to see the full error trace

if __name__ == "__main__":
    logger.info("Creating initial data")
    init_db()
    logger.info("Initial data created") 