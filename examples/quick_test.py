"""
Quick test script to verify the API is working.

Usage:
    python examples/quick_test.py
"""
import requests
import json


def test_api(base_url="http://localhost:8000"):
    """Test the API endpoints."""
    print("🧪 Testing Gen Z Slang Explainer API\n")

    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("   ✅ Health check passed\n")
        else:
            print(f"   ❌ Health check failed: {response.status_code}\n")
            return
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Could not connect to API at {base_url}")
        print("   Make sure the API is running with: uvicorn src.router:app --reload\n")
        return

    # Test 2: Explain endpoint
    test_terms = ["u", "stan", "jk", "sis", "lmao", "ngl", "irl", "idc"]

    print("2. Testing explain endpoint with sample terms...\n")
    for term in test_terms:
        print(f"   Testing term: '{term}'")
        try:
            response = requests.post(
                f"{base_url}/v1/explain",
                json={"term": term},
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Definition: {data.get('definition', 'N/A')}")
                print(f"      Example: {data.get('example', 'N/A')}")
                print(f"      Source: {data.get('source', 'N/A')}\n")
            else:
                print(f"   ❌ Failed: {response.status_code} - {response.text}\n")

        except Exception as e:
            print(f"   ❌ Error: {str(e)}\n")

    print("✨ Testing complete!")


if __name__ == "__main__":
    # You can change the base URL here if needed
    API_URL = "http://localhost:8000"
    test_api(API_URL)
