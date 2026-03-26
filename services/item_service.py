from sqlalchemy.orm import Session

from models.item import Item
from utils.logger import LoggerUtils


logger = LoggerUtils.get_logger(__name__)


class ItemService:
    def __init__(self, db: Session):
        self.db = db

    def create_item(self, item: Item) -> Item:
        """
        Placeholder create flow. Replace this with ORM persistence logic
        once item models and repositories are added.
        """
        logger.info(f"Creating item: {item}")
        return item

    def get_item(self, item_id: int, q: str | None = None) -> dict[str, int | str | None]:
        """
        Placeholder read flow. Replace this with a database query once
        item persistence is implemented.
        """
        logger.info(f"Fetching item_id={item_id}, q={q}")
        return {"item_id": item_id, "q": q}
