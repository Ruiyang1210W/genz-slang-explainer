"""Tests for retrieval module."""

import os
import pytest
import tempfile
import json


class TestRetrieval:
    """Test the retrieval module."""

    @pytest.fixture
    def test_data_file(self):
        """Create a temporary test data file."""
        # Create a temporary file with test data
        test_data = [
            {"term": "rizz", "definition": "Charisma", "example": "He's got rizz"},
            {"term": "no cap", "definition": "No lie", "example": "That's true, no cap"},
            {"term": "bussin", "definition": "Really good", "example": "This is bussin"},
        ]

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".jsonl", encoding="utf-8"
        ) as f:
            for item in test_data:
                f.write(json.dumps(item) + "\n")
            temp_path = f.name

        yield temp_path

        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    def test_lookup_existing_term(self, test_data_file, monkeypatch):
        """Test looking up a term that exists in the lexicon."""
        # Set the environment variable to use our test file
        monkeypatch.setenv("SLANG_DATA", test_data_file)

        # Need to reimport to get the new environment variable
        import importlib
        from src import retrieval

        importlib.reload(retrieval)

        result = retrieval.lookup("rizz")

        assert result is not None
        assert result["definition"] == "Charisma"
        assert result["example"] == "He's got rizz"

    def test_lookup_case_insensitive(self, test_data_file, monkeypatch):
        """Test that lookup is case insensitive."""
        monkeypatch.setenv("SLANG_DATA", test_data_file)

        import importlib
        from src import retrieval

        importlib.reload(retrieval)

        result1 = retrieval.lookup("RIZZ")
        result2 = retrieval.lookup("rizz")
        result3 = retrieval.lookup("RiZz")

        assert result1 == result2 == result3
        assert result1 is not None

    def test_lookup_with_whitespace(self, test_data_file, monkeypatch):
        """Test that lookup handles whitespace."""
        monkeypatch.setenv("SLANG_DATA", test_data_file)

        import importlib
        from src import retrieval

        importlib.reload(retrieval)

        result = retrieval.lookup("  rizz  ")

        assert result is not None
        assert result["definition"] == "Charisma"

    def test_lookup_multiword_term(self, test_data_file, monkeypatch):
        """Test looking up multi-word terms."""
        monkeypatch.setenv("SLANG_DATA", test_data_file)

        import importlib
        from src import retrieval

        importlib.reload(retrieval)

        result = retrieval.lookup("no cap")

        assert result is not None
        assert result["definition"] == "No lie"

    def test_lookup_nonexistent_term(self, test_data_file, monkeypatch):
        """Test looking up a term that doesn't exist."""
        monkeypatch.setenv("SLANG_DATA", test_data_file)

        import importlib
        from src import retrieval

        importlib.reload(retrieval)

        result = retrieval.lookup("nonexistent")

        assert result is None

    def test_load_lexicon_missing_file(self, monkeypatch):
        """Test loading lexicon when file doesn't exist."""
        monkeypatch.setenv("SLANG_DATA", "/nonexistent/path/file.jsonl")

        from src import retrieval

        lexicon = retrieval._load_lexicon()

        # Should return empty dict, not crash
        assert lexicon == {}

    def test_load_lexicon_empty_lines(self, monkeypatch):
        """Test that empty lines in JSONL are skipped."""
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".jsonl", encoding="utf-8"
        ) as f:
            f.write('{"term": "test", "definition": "Test def", "example": "Test ex"}\n')
            f.write("\n")  # Empty line
            f.write('{"term": "test2", "definition": "Test def 2", "example": "Test ex 2"}\n')
            temp_path = f.name

        try:
            monkeypatch.setenv("SLANG_DATA", temp_path)

            import importlib
            from src import retrieval

            importlib.reload(retrieval)

            assert len(retrieval._LEX) == 2
            assert "test" in retrieval._LEX
            assert "test2" in retrieval._LEX
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_lookup_returns_none_for_empty_term(self):
        """Test that lookup returns None for empty string."""
        from src.retrieval import lookup

        result = lookup("")
        assert result is None

        result = lookup("   ")
        # This might return None or find a match - depends on data
        # Just verify it doesn't crash
