from app.utils.exporters import export_csv, export_json


def test_export_csv_includes_header_and_rows() -> None:
    content = export_csv([{"website": "Amazon", "title": "Mouse"}]).decode("utf-8")
    assert "website,title" in content
    assert "Amazon,Mouse" in content


def test_export_json_returns_pretty_json() -> None:
    content = export_json([{"website": "Amazon", "title": "Mouse"}]).decode("utf-8")
    assert '"website": "Amazon"' in content
