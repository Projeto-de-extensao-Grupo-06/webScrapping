from typing import List

import src.config.db as mysql
from src.entity.material_url import MaterialUrl


def get_materials_url_with_cursor(size=10, cursor=0) -> List[MaterialUrl]:
    query = """
        SELECT id_material_url, url, price
        FROM material_url
        WHERE id_material_url > %s
        ORDER BY id_material_url
        LIMIT %s
    """

    rows = mysql.select(query, (cursor, size))

    result: List[MaterialUrl] = []

    for row in rows:
        id_material_url = row.get("id_material_url")
        url = row.get("url")
        price = row.get("price")

        result.append(MaterialUrl(id_material_url, url, price))


    return result


def update_many_material_url(material_urls: List[MaterialUrl]):
    query = "UPDATE material_url SET price = %s WHERE id_material_url = %s"

    updates = []

    for material_url in material_urls:
        updates.append({
            "query": query,
            "parameters": (material_url.price, material_url.id_material_url)
        })

    mysql.write_many(updates)



