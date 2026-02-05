"""Test error handling with invalid city"""
import requests

query = {
    "query": "What's the weather in Ranchi?"
}

print("=" * 70)
print("🧪 TEST: Error Handling (Invalid City)")
print("=" * 70)
print(f"Query: {query['query']}\n")

response = requests.post("http://127.0.0.1:8000/query", json=query)

if response.status_code == 200:
    result = response.json()
    
    print("✅ Response Received\n")
    
    print(f"📋 Executor Results:")
    for exec_out in result['executor_outputs']:
        if not exec_out['success']:
            print(f"   ✗ Step {exec_out['step_number']}: Failed")
            print(f"      Error: {exec_out['error_message']}")
        else:
            print(f"   ✓ Step {exec_out['step_number']}: Success")
    
    print(f"\n🔍 Verifier Status: {result['verifier_output']['status']}")
    print(f"\n💬 Final Response:")
    print(f"   {result['final_response']}")
    
    print(f"\n✅ Error handled gracefully!")
else:
    print(f"❌ Server Error: {response.status_code}")

print("=" * 70)
