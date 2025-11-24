# Examples

This directory contains example scripts for testing and using the Gen Z Slang Explainer API.

## Quick Test Script

**File**: `quick_test.py`

A simple script to verify the API is working correctly.

**Usage:**
```bash
# Make sure the API is running first
cd api
uvicorn src.router:app --reload

# In another terminal, run the test script
python examples/quick_test.py
```

**What it does:**
- Tests the health endpoint
- Sends sample slang terms to the explain endpoint
- Displays the results in a readable format

## Using with Python Requests

```python
import requests

# Explain a term
response = requests.post(
    "http://localhost:8000/v1/explain",
    json={"term": "jk"}
)

result = response.json()
print(f"Definition: {result['definition']}")
print(f"Example: {result['example']}")
```

## Recommended Test Terms

These terms have been tested and produce good results:
- **Common abbreviations**: u, jk, ngl, irl, idc, asap, ez, idk, ty, sry, plz, ppl
- **Slang**: stan, sis, lmao
- **Internet terms**: nsfw, ootd
