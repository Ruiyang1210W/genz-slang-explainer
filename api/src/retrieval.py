import json
import os
import logging

logger = logging.getLogger(__name__)

DATA = os.getenv(
    "SLANG_DATA", os.path.join(os.path.dirname(__file__), "..", "data", "slang_pairs.jsonl")
)


def _load_lexicon():
    """
    Load slang lexicon from JSONL file.

    Returns:
        dict: Dictionary mapping terms to their definitions and examples

    Raises:
        No exceptions - returns empty dict if file not found or invalid
    """
    lex = {}
    try:
        logger.info(f"Loading lexicon from: {DATA}")
        with open(DATA, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    r = json.loads(line)
                    term = r["term"].strip().lower()
                    lex[term] = {
                        "definition": r["definition"].strip(),
                        "example": r["example"].strip(),
                    }
                except (json.JSONDecodeError, KeyError) as e:
                    logger.warning(f"Skipping invalid line {line_num} in {DATA}: {e}")
                    continue

        logger.info(f"Loaded {len(lex)} terms from lexicon")
    except FileNotFoundError:
        logger.warning(f"Lexicon file not found: {DATA}. Starting with empty lexicon.")
    except Exception as e:
        logger.error(f"Error loading lexicon: {str(e)}", exc_info=True)

    return lex


_LEX = _load_lexicon()


def lookup(term: str):
    """
    Look up a slang term in the lexicon.

    Args:
        term: The slang term to look up

    Returns:
        dict or None: Dictionary with 'definition' and 'example' keys, or None if not found
    """
    if not term:
        return None

    normalized_term = term.strip().lower()
    result = _LEX.get(normalized_term)

    if result:
        logger.debug(f"Found term in lexicon: {normalized_term}")
    else:
        logger.debug(f"Term not found in lexicon: {normalized_term}")

    return result
