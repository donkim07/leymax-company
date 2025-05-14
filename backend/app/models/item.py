from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum

class ItemType(str, enum.Enum):
    RAW_MATERIAL = "raw_material"
    FINISHED_GOOD = "finished_good"
    TOOL = "tool"

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    barcode = Column(String(50), unique=True)
    type = Column(Enum(ItemType), nullable=False)
    unit_type = Column(String(20), nullable=False)  # e.g., kg, pcs, etc.
    category_id = Column(Integer, ForeignKey("categories.id"))
    cost_price = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)
    tax_rate = Column(Float, default=0.0)
    image_url = Column(String(255))
    reorder_point = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("Company")
    category = relationship("Category")
    inventory = relationship("Inventory", back_populates="item")
    recipe_ingredients = relationship("RecipeIngredient", back_populates="item")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("Company")
    parent = relationship("Category", remote_side=[id], backref="subcategories")
