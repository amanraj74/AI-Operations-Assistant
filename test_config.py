"""Quick test to verify API keys"""
from llm.config import Config

try:
    Config.validate()
    print("✓ All API keys loaded successfully!")
    print(f"✓ Gemini API: {Config.GEMINI_API_KEY[:20]}...")
    print(f"✓ Weather API: {Config.OPENWEATHER_API_KEY[:20]}...")
    print(f"✓ News API: {Config.NEWS_API_KEY[:20]}...")
except Exception as e:
    print(f"✗ Error: {e}")
