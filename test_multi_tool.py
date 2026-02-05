"""Test multi-tool query - Uses BOTH weather and news APIs"""
import requests
import json
import time

query = {
    "query": "Plan a weekend date in Mumbai - check weather and events"
}

print("=" * 70)
print("🧪 TEST: Multi-Tool Query (Weather + News)")
print("=" * 70)
print(f"Query: {query['query']}\n")

start = time.time()
response = requests.post("http://127.0.0.1:8000/query", json=query)
elapsed = time.time() - start

if response.status_code == 200:
    result = response.json()
    
    print("✅ SUCCESS!\n")
    print(f"📊 Request ID: {result['request_id']}")
    print(f"⏱️  Total Time: {result['total_execution_time']}s")
    
    print(f"\n🧠 PLANNER AGENT:")
    print(f"   Intent: {result['planner_output']['user_intent']}")
    print(f"   Complexity: {result['planner_output']['estimated_complexity']}")
    print(f"   Steps: {len(result['planner_output']['plan_steps'])}")
    
    for step in result['planner_output']['plan_steps']:
        print(f"\n   Step {step['step_number']}: {step['description']}")
        print(f"   → Tool: {step['tool_required']}")
        print(f"   → Params: {step['parameters']}")
    
    print(f"\n⚙️  EXECUTOR AGENT:")
    success_count = sum(1 for e in result['executor_outputs'] if e['success'])
    print(f"   Executed: {len(result['executor_outputs'])} steps")
    print(f"   Success Rate: {success_count}/{len(result['executor_outputs'])}")
    
    for exec_out in result['executor_outputs']:
        status = "✓" if exec_out['success'] else "✗"
        print(f"\n   {status} Step {exec_out['step_number']} ({exec_out['tool_used'].upper()})")
        print(f"      Time: {exec_out['execution_time']}s")
        if exec_out['success']:
            print(f"      Data Keys: {list(exec_out['data'].keys())}")
        else:
            print(f"      Error: {exec_out['error_message']}")
    
    print(f"\n🔍 VERIFIER AGENT:")
    print(f"   Status: {result['verifier_output']['status'].upper()}")
    print(f"   Confidence: {result['verifier_output']['confidence_score']:.2%}")
    if result['verifier_output']['issues_found']:
        print(f"   Issues: {result['verifier_output']['issues_found']}")
    
    print(f"\n💬 FINAL RESPONSE:")
    print("   " + "-" * 66)
    print(f"   {result['final_response']}")
    print("   " + "-" * 66)
    
    print(f"\n✅ Test Passed!")
else:
    print(f"❌ FAILED: {response.status_code}")
    print(response.text)

print("=" * 70)
