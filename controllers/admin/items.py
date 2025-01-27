from fastapi import APIRouter, Depends
from typing import Union, Dict
from utils.logger import logger
from models.item import Item
from models.response import APISuccessResponse
from auth.auth_handler import AuthHandler

router = APIRouter()
auth_handler = AuthHandler()

@router.post("")
def create_item(item: Item, current_user: Dict[str, str] | None = Depends(auth_handler.get_current_user)):
    logger.info(f"item: {item}")
    return APISuccessResponse(data=item)

@router.get("/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None, current_user: Dict[str, str] | None = Depends(auth_handler.get_current_user)):
    data = {"item_id": item_id, "q": q}
    return APISuccessResponse(data=data)