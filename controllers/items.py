from fastapi import APIRouter
from typing import Union
from utils.logger import logger
from models.item import Item
from models.response import APISuccessResponse

router = APIRouter()

@router.post("")
def create_item(item: Item):
    logger.info(f"item: {item}")
    return APISuccessResponse(data=item)

@router.get("/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    data = {"item_id": item_id, "q": q}
    return APISuccessResponse(data=data)