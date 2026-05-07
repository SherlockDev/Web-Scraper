from app.models import DataField, ScrapeRequest, Website


def test_request_deduplicates_multiselect_values() -> None:
    payload = ScrapeRequest(
        websites=[Website.amazon, Website.amazon, Website.ebay],
        query="wireless mouse",
        fields=[DataField.title, DataField.title, DataField.price],
    )

    assert payload.websites == [Website.amazon, Website.ebay]
    assert payload.fields == [DataField.title, DataField.price]
