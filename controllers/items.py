from fastapi import APIRouter
from typing import Union
from utils.logger import logger
from models.item import Item

router = APIRouter()

@router.post("")
def create_item(item: Item):
    logger.info(f"item: {item}")
    return {"item_price:": item.price}

@router.get("/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}