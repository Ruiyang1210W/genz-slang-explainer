"""Post-processing utilities for parsing model outputs."""
import re
import logging

logger = logging.getLogger(__name__)


def parse_definition_example(text: str):
    """
    Parse definition and example from model-generated text.

    Expected format:
        Definition: <definition text>
        Example: <example text>

    Args:
        text: Model-generated text containing definition and example

    Returns:
        dict: Dictionary with keys:
            - definition (str or None): Extracted definition
            - example (str or None): Extracted example
            - format_ok (bool): True if both definition and example were found
    """
    defn = re.search(r"Definition:\s*(.+)", text, re.I)
    ex = re.search(r"Example:\s*(.+)", text, re.I)

    result = {
        "definition": defn.group(1).strip() if defn else None,
        "example": ex.group(1).strip() if ex else None,
        "format_ok": bool(defn and ex),
    }

    if not result["format_ok"]:
        logger.debug(f"Parse incomplete - definition: {bool(defn)}, example: {bool(ex)}")

    return result
