from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Float, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum

class CompanyType(str, enum.Enum):
    BAKERY = "bakery"
    TOOLS = "tools"
    ACADEMY = "academy"

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum(CompanyType), nullable=False)
    description = Column(Text)
    address = Column(String(255))
    phone = Column(String(20))
    email = Column(String(100))
    logo_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    stores = relationship("Store", back_populates="company")
    users = relationship("User", back_populates="company")

class StoreType(str, enum.Enum):
    MAIN = "main"
    SUB = "sub"

class Store(Base):
    __tablename__ = "stores"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    parent_store_id = Column(Integer, ForeignKey("stores.id"), nullable=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum(StoreType), nullable=False)
    address = Column(String(255))
    phone = Column(String(20))
    email = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="stores")
    parent_store = relationship("Store", remote_side=[id], backref="sub_stores")
    inventory = relationship("Inventory", back_populates="store")
    sales = relationship("Sale", back_populates="store")
