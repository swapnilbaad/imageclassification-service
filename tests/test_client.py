import pytest
import asyncio
import zmq.asyncio
from src.client import parse_csv

@pytest.mark.asyncio
async def test_parse_csv(tmp_path):
    csv_content = "http://example.com/image1.jpg\nhttp://example.com/image2.jpg\n"
    file_path = tmp_path / "test_urls.csv"
    file_path.write_text(csv_content)
    urls = parse_csv(str(file_path))
    assert isinstance(urls, list)
    assert len(urls) == 2
    assert urls[0] == "http://example.com/image1.jpg"