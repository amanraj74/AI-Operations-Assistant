"""Test news-only query"""
import requests
import json

query = {
    "query": "Show me latest entertainment news in India"
}

print("=" * 70)
print("🧪 TEST: News API Only")
print("=" * 70)
print(f"Query: {query['query']}\n")

response = requests.post("http://127.0.0.1:8000/query", json=query)

if response.status_code == 200:
    result = response.json()
    
    print("✅ SUCCESS!\n")
    print(f"📊 Request ID: {result['request_id']}")
    
    print(f"\n📋 Plan Steps:")
    for step in result['planner_output']['plan_steps']:
        print(f"   • {step['description']} [{step['tool_required']}]")
    
    print(f"\n📰 News Data:")
    for exec_out in result['executor_outputs']:
        if exec_out['success'] and exec_out['tool_used'] == 'news':
            data = exec_out['data'].get('data', {})
            articles = data.get('articles', [])
            print(f"   Found {len(articles)} articles")
            for i, article in enumerate(articles[:3], 1):
                print(f"\n   {i}. {article['title']}")
                print(f"      Source: {article['source']}")
    
    print(f"\n💬 Final Response:")
    print(f"   {result['final_response'][:300]}...")
    
    print(f"\n✅ Test Passed!")
else:
    print(f"❌ FAILED: {response.status_code}")
    print(response.text)

print("=" * 70)
