"""Tests for API router endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock


class TestAPIEndpoints:
    """Test the API endpoints."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        from src.router import app
        return TestClient(app)

    def test_index_endpoint(self, client):
        """Test the root index endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "slang-explainer"
        assert data["status"] == "ok"

    def test_health_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["ok"] is True

    @patch("src.router.generate")
    @patch("src.router.parse_definition_example")
    def test_explain_endpoint_success(self, mock_parse, mock_generate, client):
        """Test the explain endpoint with successful generation."""
        # Mock the generate function to return a formatted response
        mock_generate.return_value = "Definition: Cool slang\nExample: That's so cool"

        # Mock the parse function to return parsed data
        mock_parse.return_value = {
            "definition": "Cool slang",
            "example": "That's so cool",
            "format_ok": True
        }

        response = client.post("/v1/explain", json={"term": "cool"})

        assert response.status_code == 200
        data = response.json()
        assert data["term"] == "cool"
        assert data["definition"] == "Cool slang"
        assert data["example"] == "That's so cool"
        assert data["source"] == "lora"

        # Verify the mocks were called correctly
        mock_generate.assert_called_once_with("cool")

    @patch("src.router.generate")
    @patch("src.router.parse_definition_example")
    @patch("src.router.lookup")
    def test_explain_endpoint_with_fallback(self, mock_lookup, mock_parse, mock_generate, client):
        """Test the explain endpoint falling back to baseline."""
        # Mock generate to return unparseable text
        mock_generate.return_value = "Some unparseable text"

        # Mock parse to indicate format is not ok
        mock_parse.return_value = {
            "definition": None,
            "example": None,
            "format_ok": False
        }

        # Mock lookup to return baseline data
        mock_lookup.return_value = {
            "definition": "Baseline definition",
            "example": "Baseline example"
        }

        response = client.post("/v1/explain", json={"term": "test"})

        assert response.status_code == 200
        data = response.json()
        assert data["term"] == "test"
        assert data["definition"] == "Baseline definition"
        assert data["example"] == "Baseline example"
        assert data["source"] == "lora+baseline"

    @patch("src.router.generate")
    @patch("src.router.parse_definition_example")
    @patch("src.router.lookup")
    def test_explain_endpoint_no_fallback(self, mock_lookup, mock_parse, mock_generate, client):
        """Test the explain endpoint when fallback also fails."""
        # Mock generate to return unparseable text
        mock_generate.return_value = "Some unparseable text"

        # Mock parse to indicate format is not ok
        mock_parse.return_value = {
            "definition": None,
            "example": None,
            "format_ok": False
        }

        # Mock lookup to return None (no baseline match)
        mock_lookup.return_value = None

        response = client.post("/v1/explain", json={"term": "unknown"})

        assert response.status_code == 200
        data = response.json()
        assert data["term"] == "unknown"
        assert data["source"] == "lora_raw"

    def test_explain_endpoint_case_normalization(self, client):
        """Test that the endpoint normalizes term case."""
        with patch("src.router.generate") as mock_generate, \
             patch("src.router.parse_definition_example") as mock_parse:

            mock_generate.return_value = "Definition: Test\nExample: Test"
            mock_parse.return_value = {
                "definition": "Test",
                "example": "Test",
                "format_ok": True
            }

            response = client.post("/v1/explain", json={"term": "  UPPERCASE  "})

            assert response.status_code == 200
            data = response.json()
            # Term should be lowercased and stripped
            assert data["term"] == "uppercase"

            # Verify generate was called with normalized term
            mock_generate.assert_called_once_with("uppercase")

    def test_explain_endpoint_validation(self, client):
        """Test that the endpoint validates input."""
        # Missing term field
        response = client.post("/v1/explain", json={})

        assert response.status_code == 422  # Validation error

    def test_explain_endpoint_empty_term(self, client):
        """Test handling of empty term."""
        # Test with whitespace-only term - should return 400 after stripping
        response = client.post("/v1/explain", json={"term": "   "})

        # After stripping, the term is empty, so it should raise a 400 error
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()
