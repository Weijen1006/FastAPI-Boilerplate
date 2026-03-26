from fastapi import APIRouter, Depends
from models.item import Item
from models.response import APISuccessResponse
from auth.auth_handler import get_current_user
from models.user import UserData, UserRoleEnum
from middlewares.auth_handler import with_role
from sqlalchemy.orm import Session
from configs.database import get_db
from services.item_service import ItemService

router = APIRouter()

@router.post("")
@with_role(UserRoleEnum.SUPER_ADMIN.value)
def create_item(
    item: Item,
    db: Session = Depends(get_db),
    current_user: UserData = Depends(get_current_user),
):
    item_service = ItemService(db)
    created_item = item_service.create_item(item)
    return APISuccessResponse(data=created_item)

@router.get("/{item_id}")
def read_item(
    item_id: int,
    db: Session = Depends(get_db),
    q: str | None = None,
    current_user: UserData = Depends(get_current_user),
):
    item_service = ItemService(db)
    item_data = item_service.get_item(item_id=item_id, q=q)
    return APISuccessResponse(data=item_data)
