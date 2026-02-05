"""
Configuration module for LLM and API settings
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    
    # App Settings
    APP_NAME = "AI Operations Assistant"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # API URLs
    OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
    NEWS_API_BASE_URL = "https://api.thenewsapi.com/v1/news"
    
    # LLM Settings
    GEMINI_MODEL = "gemini-2.5-flash"
    MAX_TOKENS = 8192
    TEMPERATURE = 0.7
    
    @classmethod
    def validate(cls):
        """Validate API keys"""
        missing = []
        if not cls.GEMINI_API_KEY or cls.GEMINI_API_KEY == "your_gemini_api_key_here":
            missing.append("GEMINI_API_KEY")
        if not cls.OPENWEATHER_API_KEY or cls.OPENWEATHER_API_KEY == "your_openweather_api_key_here":
            missing.append("OPENWEATHER_API_KEY")
        if not cls.NEWS_API_KEY or cls.NEWS_API_KEY == "your_news_api_key_here":
            missing.append("NEWS_API_KEY")
        
        if missing:
            raise ValueError(f"Missing API keys: {', '.join(missing)}")
        return True
