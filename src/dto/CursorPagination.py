from typing import List

from src.entity.material_url import MaterialUrl


class CursorPagination:
    def __init__(self, items: List[MaterialUrl], cursor: str = None, size: int = 0):
        self.items = items
        self.next_cursor = cursor
        self.size = size