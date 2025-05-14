from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud.crud_order import crud_order
from app.schemas.order import Order, OrderCreate, OrderUpdate, OrderItem, OrderItemCreate

router = APIRouter()

@router.get("/", response_model=List[Order])
def read_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """
    Retrieve orders for the current user's company.
    """
    if current_user.role == "admin":
        orders = crud_order.get_multi_by_company(
            db=db, company_id=current_user.company_id, skip=skip, limit=limit
        )
    else:
        orders = crud_order.get_multi_by_store(
            db=db, store_id=current_user.store_id, skip=skip, limit=limit
        )
    return orders

@router.post("/", response_model=Order)
def create_order(
    *,
    db: Session = Depends(deps.get_db),
    order_in: OrderCreate,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """
    Create new order.
    """
    order_in.company_id = current_user.company_id
    order_in.store_id = current_user.store_id
    order_in.user_id = current_user.id
    order = crud_order.create(db=db, obj_in=order_in)
    return order

@router.put("/{order_id}", response_model=Order)
def update_order(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
    order_in: OrderUpdate,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """
    Update an order.
    """
    order = crud_order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if order.store_id != current_user.store_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    order = crud_order.update(db=db, db_obj=order, obj_in=order_in)
    return order

@router.get("/{order_id}", response_model=Order)
def read_order(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get order by ID.
    """
    order = crud_order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if order.store_id != current_user.store_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return order

@router.delete("/{order_id}")
def delete_order(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """
    Delete an order.
    """
    order = crud_order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    crud_order.remove(db=db, id=order_id)
    return {"message": "Order deleted successfully"} 