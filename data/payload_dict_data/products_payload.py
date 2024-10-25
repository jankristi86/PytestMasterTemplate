SIMPLE_PRODUCT_PAYLOAD = {
    "name": dict[str] | None,
    "type": dict[str] | None,
    "regular_price": dict[str] | None,
    "description": None,
    "short_description": None,
    "categories": None,
    "images": None
}

UPDATE_PRODUCT_PRICE_PAYLOAD = {
    "regular_price": dict[str] | None
}
