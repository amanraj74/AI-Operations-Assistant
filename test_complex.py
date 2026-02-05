"""Test complex multi-agent query"""
import requests
import json

query = {
    "query": "Plan a romantic date in Mumbai this weekend"
}

print("🧪 Testing Complex Multi-Agent Query...")
print(f"Query: {query['query']}\n")

response = requests.post(
    "http://127.0.0.1:8000/query",
    json=query
)

if response.status_code == 200:
    result = response.json()
    print("✅ SUCCESS!")
    print(f"\n🤖 Planner Intent: {result['planner_output']['user_intent']}")
    print(f"\n📋 Plan Steps: {len(result['planner_output']['plan_steps'])} steps")
    for step in result['planner_output']['plan_steps']:
        print(f"  Step {step['step_number']}: {step['description']} [Tool: {step['tool_required']}]")
    
    print(f"\n⚙️  Execution Results:")
    for exec_out in result['executor_outputs']:
        status = "✓" if exec_out['success'] else "✗"
        print(f"  {status} Step {exec_out['step_number']} ({exec_out['tool_used']}): {exec_out['execution_time']}s")
    
    print(f"\n🔍 Verification Status: {result['verifier_output']['status']}")
    print(f"📈 Confidence: {result['verifier_output']['confidence_score']}")
    
    print(f"\n💬 Final Response:")
    print(result['final_response'])
else:
    print(f"❌ FAILED: {response.status_code}")
    print(response.text)
