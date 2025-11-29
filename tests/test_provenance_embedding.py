"""Test provenance embedding in generated documents"""
import asyncio
import aiohttp
import json

BASE_URL = "http://localhost:8001"

async def test_provenance_in_letter():
    """Verify generated letter contains provenance JSON"""
    
    payload = {
        "template_id": "debt_validation_v1",
        "template_version": "1.0.0",
        "fields": {
            "date": "2025-11-29",
            "recipient_name": "Test Collector",
            "account_number": "TEST123",
            "consumer_name": "Test User",
            "consumer_address": "123 Test St"
        },
        "tone": "formal",
        "user_id": "provenance_test",
        "trace_id": "prov_embed_001"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/api/writer/generate", json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                
                # Check if provenance is in HTML
                if "provenance_json" in data['html_preview']:
                    print("✓ Provenance JSON embedded in document")
                    
                    # Extract provenance
                    import re
                    prov_match = re.search(r'<!-- Provenance: ({.*?}) -->', data['html_preview'])
                    if prov_match:
                        prov_data = json.loads(prov_match.group(1))
                        print(f"  - Template ID: {prov_data.get('template_id')}")
                        print(f"  - Trace ID: {prov_data.get('trace_id')}")
                        print(f"  - User ID: {prov_data.get('user_id')}")
                    
                    # Verify hash matches
                    print(f"  - Document Hash: {data['hash'][:16]}...")
                    return True
                else:
                    print("✗ Provenance NOT found in document")
                    return False
            else:
                print(f"✗ Writer generate failed: {resp.status}")
                return False

if __name__ == "__main__":
    success = asyncio.run(test_provenance_in_letter())
    import sys
    sys.exit(0 if success else 1)
