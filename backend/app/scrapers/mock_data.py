from app.models import Product


def build_mock_product(website: str, query: str, page: int) -> Product:
    return Product(
        website=website,
        title=f"{query.title()} - {website} Result {page}",
        price=f"${49 + page}.99",
        rating="4.5",
        reviews_count=str(100 * page),
        product_url=f"https://example.com/{website.lower()}/{query.replace(' ', '-')}/{page}",
        product_image="https://picsum.photos/200",
        seller=f"{website} Store",
        availability="In stock",
    )
