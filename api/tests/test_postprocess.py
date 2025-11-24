"""Tests for postprocess module."""
from src.postprocess import parse_definition_example


class TestParseDefinitionExample:
    """Test the parse_definition_example function."""

    def test_parse_valid_format(self):
        """Test parsing text with both definition and example."""
        text = """Task: Explain the internet slang.
Term: rizz

Definition: Charisma or charm used to attract someone
Example: He's got so much rizz, everyone wants to talk to him"""

        result = parse_definition_example(text)

        assert result["format_ok"] is True
        assert result["definition"] == "Charisma or charm used to attract someone"
        assert result["example"] == "He's got so much rizz, everyone wants to talk to him"

    def test_parse_definition_only(self):
        """Test parsing text with only definition."""
        text = "Definition: Something cool"

        result = parse_definition_example(text)

        assert result["format_ok"] is False
        assert result["definition"] == "Something cool"
        assert result["example"] is None

    def test_parse_example_only(self):
        """Test parsing text with only example."""
        text = "Example: This is an example"

        result = parse_definition_example(text)

        assert result["format_ok"] is False
        assert result["definition"] is None
        assert result["example"] == "This is an example"

    def test_parse_no_matches(self):
        """Test parsing text with neither definition nor example."""
        text = "Just some random text without proper format"

        result = parse_definition_example(text)

        assert result["format_ok"] is False
        assert result["definition"] is None
        assert result["example"] is None

    def test_parse_case_insensitive(self):
        """Test that parsing is case insensitive."""
        text = "definition: Test definition\nexample: Test example"

        result = parse_definition_example(text)

        assert result["format_ok"] is True
        assert result["definition"] == "Test definition"
        assert result["example"] == "Test example"

    def test_parse_multiline(self):
        """Test parsing multiline content."""
        text = """
        Some preamble text
        Definition: A cool slang term
        Some middle text
        Example: That's so cool!
        """

        result = parse_definition_example(text)

        assert result["format_ok"] is True
        assert result["definition"] == "A cool slang term"
        assert result["example"] == "That's so cool!"

    def test_parse_with_extra_whitespace(self):
        """Test that extra whitespace is stripped."""
        text = "Definition:   Lots of spaces   \nExample:   More spaces   "

        result = parse_definition_example(text)

        assert result["definition"] == "Lots of spaces"
        assert result["example"] == "More spaces"
