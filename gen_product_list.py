import json
from db import Product


def gen_product_list():
    products: list[Product] = Product.objects.only(
        "name", "condition", "category", "description",
        "gender", "price", "countInStock", "sizes"
    )

    with open('product_list.json', 'w', encoding="utf-8") as w:
         w.write(json.dumps([{
            "name": x.name,
            "condition": x.condition,
            "category": x.category,
            "description": x.description,
            "gender": x.gender,
            "price": x.price,
            "countInStock": x.countInStock,
            "sizes": [{"name": t["name"], "count": t["count"]} for t in x.sizes]
         } for x in products], ensure_ascii=False, indent=4))
