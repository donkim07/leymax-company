from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging
import pymysql

# Register PyMySQL as the MySQL driver
pymysql.install_as_MySQLdb()

logger = logging.getLogger(__name__)

logger.debug(f"Connecting to database: {settings.DATABASE_URL}")
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=True,  # Enable SQL logging
    connect_args={
        "charset": "utf8mb4"
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        logger.debug("Creating new database session")
        yield db
    finally:
        logger.debug("Closing database session")
        db.close()
