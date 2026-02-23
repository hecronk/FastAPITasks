from unittest.mock import patch, MagicMock
from src.services.random_number import get_random_numbers

def test_get_random_numbers_success():
    with patch("requests.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.json.return_value = [123]
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        result = get_random_numbers(1)
        assert result["data"] == 123
        assert result["errors"] == {}

def test_get_random_numbers_invalid_count():
    result = get_random_numbers("a")
    assert result["data"] == []
    assert "must be int" in result["errors"][0]

def test_get_random_numbers_request_exception():
    with patch("requests.get", side_effect=Exception("API error")):
        result = get_random_numbers(1)
        assert result["data"] == []
        assert "API error" in result["errors"][0]
