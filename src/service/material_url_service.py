from typing import List

from src.dto.CursorPagination import CursorPagination
from src.repository.material_url_repository import get_materials_url_with_cursor

def get_all_material_url_cursor(cursor: int = 0, size: int = None) -> CursorPagination:
    materials_url = get_materials_url_with_cursor(size=size, cursor=cursor)

    result_size = len(materials_url)


    if result_size < size or result_size == 0:
        next_cursor = None
    else:
        next_cursor = materials_url[-1].id_material_url

    return CursorPagination(materials_url, next_cursor, size=result_size)

