"""
News API Tool - TheNewsAPI Integration
"""
import httpx
from datetime import datetime
from typing import Optional, Dict, Any, List
from llm.config import Config
from llm.response_models import NewsArticle


class NewsTool:
    """Tool for fetching news and events from TheNewsAPI"""
    
    def __init__(self):
        """Initialize News Tool with API configuration"""
        self.api_key = Config.NEWS_API_KEY
        self.base_url = Config.NEWS_API_BASE_URL
        self.timeout = 10.0
    
    async def get_news(
        self,
        query: str,
        country: str = "in",
        language: str = "en",
        limit: int = 5
    ) -> Dict[str, Any]:
        """
        Get news articles based on search query
        
        Args:
            query: Search keywords (e.g., "Mumbai events", "technology")
            country: Country code (default: "in" for India)
            language: Language code (default: "en")
            limit: Maximum number of articles to return
            
        Returns:
            Dictionary containing news articles or error
        """
        try:
            url = f"{self.base_url}/all"
            
            params = {
                "api_token": self.api_key,
                "search": query,
                "language": language,
                "countries": country,
                "limit": limit
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
            
            # Parse articles
            articles = []
            if data.get('data'):
                for item in data['data']:
                    article = NewsArticle(
                        title=item.get('title', 'No title'),
                        description=item.get('description', 'No description available'),
                        url=item.get('url', ''),
                        published_at=item.get('published_at', datetime.now().isoformat()),
                        source=item.get('source', 'Unknown')
                    )
                    articles.append(article.model_dump())
            
            return {
                "success": True,
                "data": {
                    "query": query,
                    "total_results": len(articles),
                    "articles": articles
                }
            }
            
        except httpx.HTTPStatusError as e:
            return {
                "success": False,
                "error": f"HTTP error: {e.response.status_code}",
                "error_type": "HTTP_ERROR"
            }
        except httpx.TimeoutException:
            return {
                "success": False,
                "error": "News API request timed out",
                "error_type": "TIMEOUT"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "error_type": "UNKNOWN"
            }
    
    async def get_top_headlines(
        self,
        category: Optional[str] = None,
        country: str = "in",
        limit: int = 5
    ) -> Dict[str, Any]:
        """
        Get top headlines by category
        
        Args:
            category: News category (e.g., "entertainment", "sports", "technology")
            country: Country code
            limit: Maximum number of articles
            
        Returns:
            Dictionary containing top headlines or error
        """
        try:
            url = f"{self.base_url}/top"
            
            params = {
                "api_token": self.api_key,
                "locale": country,
                "limit": limit
            }
            
            if category:
                params["categories"] = category
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
            
            # Parse headlines
            articles = []
            if data.get('data'):
                for item in data['data']:
                    article = NewsArticle(
                        title=item.get('title', 'No title'),
                        description=item.get('description', 'No description available'),
                        url=item.get('url', ''),
                        published_at=item.get('published_at', datetime.now().isoformat()),
                        source=item.get('source', 'Unknown')
                    )
                    articles.append(article.model_dump())
            
            return {
                "success": True,
                "data": {
                    "category": category or "general",
                    "total_results": len(articles),
                    "articles": articles
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Headlines error: {str(e)}",
                "error_type": "HEADLINES_ERROR"
            }
    