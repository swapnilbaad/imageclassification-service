import pytest
import asyncio
import os
import zmq.asyncio
from src.client import parse_csv

@pytest.mark.asyncio
async def test_parse_csv_valid_file(tmp_path):
    """Test parsing a valid CSV file with multiple URLs."""
    csv_content = "http://example.com/image1.jpg\nhttp://example.com/image2.jpg\n"
    file_path = tmp_path / "test_urls.csv"
    file_path.write_text(csv_content)

    urls = parse_csv(str(file_path))

    assert isinstance(urls, list)
    assert len(urls) == 2
    assert urls[0] == "http://example.com/image1.jpg"
    assert urls[1] == "http://example.com/image2.jpg"

@pytest.mark.asyncio
async def test_parse_csv_empty_file(tmp_path):
    """Test parsing an empty CSV file."""
    file_path = tmp_path / "empty.csv"
    file_path.write_text("")

    urls = parse_csv(str(file_path))

    assert isinstance(urls, list)
    assert len(urls) == 0  # Should return an empty list

@pytest.mark.asyncio
async def test_parse_csv_extra_whitespace(tmp_path):
    """Test parsing a CSV file with extra whitespace and blank lines."""
    csv_content = "  http://example.com/image1.jpg  \n\nhttp://example.com/image2.jpg   \n"
    file_path = tmp_path / "whitespace.csv"
    file_path.write_text(csv_content)

    urls = parse_csv(str(file_path))

    assert isinstance(urls, list)
    assert len(urls) == 2
    assert urls[0] == "http://example.com/image1.jpg"
    assert urls[1] == "http://example.com/image2.jpg"

@pytest.mark.asyncio
async def test_parse_csv_invalid_url(tmp_path):
    """Test parsing a CSV file with an invalid URL format."""
    csv_content = "not_a_url\nhttp://example.com/image2.jpg\n"
    file_path = tmp_path / "invalid_url.csv"
    file_path.write_text(csv_content)

    urls = parse_csv(str(file_path))

    assert isinstance(urls, list)
    assert len(urls) == 1  # Should filter out invalid URLs
    assert urls[0] == "http://example.com/image2.jpg"

@pytest.mark.asyncio
async def test_parse_csv_missing_file():
    """Test handling of a missing CSV file."""
    missing_file_path = "non_existent_file.csv"

    with pytest.raises(FileNotFoundError):
        parse_csv(missing_file_path)

@pytest.mark.asyncio
async def test_parse_csv_non_csv_file(tmp_path):
    """Test parsing a non-CSV file (e.g., JSON or text)."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("Some random text, not URLs.")

    urls = parse_csv(str(file_path))

    assert isinstance(urls, list)
    assert len(urls) == 0  # Should return an empty list

