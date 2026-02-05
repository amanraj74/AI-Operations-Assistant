"""Test all example queries"""
import requests
import time

examples = [
    "Plan a romantic date in Mumbai this weekend",
    "What's the weather like in Bangalore today?",
    "Show me latest entertainment news in India",
    "Suggest an outdoor activity in Delhi",
    "Check Goa weather and local events"
]

print("=" * 70)
print("🧪 RUNNING ALL EXAMPLE QUERIES")
print("=" * 70)

results = []

for i, query_text in enumerate(examples, 1):
    print(f"\n[{i}/{len(examples)}] Testing: {query_text}")
    
    start = time.time()
    response = requests.post(
        "http://127.0.0.1:8000/query",
        json={"query": query_text},
        timeout=30
    )
    elapsed = time.time() - start
    
    if response.status_code == 200:
        result = response.json()
        status = "✅ PASS"
        success_rate = sum(1 for e in result['executor_outputs'] if e['success']) / len(result['executor_outputs'])
    else:
        status = "❌ FAIL"
        success_rate = 0
    
    results.append({
        "query": query_text,
        "status": status,
        "time": elapsed,
        "success_rate": success_rate
    })
    
    print(f"   {status} | Time: {elapsed:.2f}s | Success Rate: {success_rate:.0%}")

print("\n" + "=" * 70)
print("📊 SUMMARY")
print("=" * 70)

passed = sum(1 for r in results if "✅" in r['status'])
avg_time = sum(r['time'] for r in results) / len(results)

print(f"\nTests Passed: {passed}/{len(results)}")
print(f"Average Response Time: {avg_time:.2f}s")
print(f"\nDetailed Results:")

for r in results:
    print(f"\n{r['status']} {r['query']}")
    print(f"   Time: {r['time']:.2f}s | Success: {r['success_rate']:.0%}")

print("\n" + "=" * 70)
