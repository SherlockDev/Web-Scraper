from app.models import DataField, Product
from app.utils.normalizer import normalize_products


def test_normalize_products_only_selected_fields() -> None:
    rows = normalize_products(
        [
            Product(
                website="Amazon",
                title="Mouse",
                price="$10",
                rating="4.1",
                product_url="https://example.com",
            )
        ],
        [DataField.title, DataField.price],
    )

    assert rows == [{"website": "Amazon", "title": "Mouse", "price": "$10"}]
