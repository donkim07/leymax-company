from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, companies, stores, items, recipes, inventory, orders, courses

api_router = APIRouter()

# Include all routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(companies.router, prefix="/companies", tags=["Companies"])
api_router.include_router(stores.router, prefix="/stores", tags=["Stores"])
api_router.include_router(items.router, prefix="/items", tags=["Items"])
api_router.include_router(recipes.router, prefix="/recipes", tags=["Recipes"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
api_router.include_router(courses.router, prefix="/courses", tags=["Academy"])
