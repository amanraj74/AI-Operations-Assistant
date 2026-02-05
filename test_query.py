"""Test the multi-agent system"""
import requests
import json

# Test query
query = {
    "query": "What's the weather in Patna today?"
}

print("🧪 Testing Multi-Agent System...")
print(f"Query: {query['query']}\n")

response = requests.post(
    "http://127.0.0.1:8000/query",
    json=query,
    headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    result = response.json()
    print("✅ SUCCESS!")
    print(f"\n📊 Request ID: {result['request_id']}")
    print(f"⏱️  Execution Time: {result['total_execution_time']}s")
    print(f"\n💬 Final Response:")
    print(result['final_response'])
    print(f"\n📋 Full Output:")
    print(json.dumps(result, indent=2))
else:
    print(f"❌ FAILED: {response.status_code}")
    print(response.text)
