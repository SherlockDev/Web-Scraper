from app.models import DataField, Product


def normalize_products(products: list[Product], selected_fields: list[DataField]) -> list[dict[str, str | None]]:
    keys = ["website", *[field.value for field in selected_fields if field.value != "website"]]
    normalized: list[dict[str, str | None]] = []

    for product in products:
        model = product.model_dump()
        normalized.append({key: model.get(key) for key in keys})

    return normalized
