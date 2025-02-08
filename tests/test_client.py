import csv
import os
import pytest
import zmq
from src.client import parse_csv

def test_parse_csv(tmp_path):
    # Create a temporary CSV file with dummy URLs.
    data = "http://example.com/image1.jpg\nhttp://example.com/image2.jpg\n"
    d = tmp_path / "sub"
    d.mkdir()
    file_path = d / "test_urls.csv"
    file_path.write_text(data)

    urls = parse_csv(str(file_path))
    assert isinstance(urls, list)
    assert len(urls) == 2
    assert urls[0] == "http://example.com/image1.jpg"
