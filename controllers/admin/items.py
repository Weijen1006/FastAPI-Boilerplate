from fastapi import APIRouter, Depends
from typing import Union, Dict
from utils.logger import logger
from models.item import Item
from models.response import APISuccessResponse
from auth.auth_handler import get_current_user
from models.user import UserData, UserRoleEnum
from middlewares.auth_handler import with_role

router = APIRouter()

@router.post("")
@with_role(UserRoleEnum.SUPER_ADMIN.value)
def create_item(item: Item, current_user: UserData = Depends(get_current_user)):
    logger.info(f"item: {item}")
    return APISuccessResponse(data=item)

@router.get("/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None, current_user: UserData = Depends(get_current_user)):
    data = {"item_id": item_id, "q": q}
    return APISuccessResponse(data=data)