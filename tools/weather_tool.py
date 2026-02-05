"""
Weather API Tool - OpenWeatherMap Integration
"""
import httpx
from datetime import datetime
from typing import Dict, Any
from llm.config import Config
from llm.response_models import WeatherData


class WeatherTool:
    """Tool for fetching weather information from OpenWeatherMap API"""
    
    def __init__(self):
        """Initialize Weather Tool with API configuration"""
        self.api_key = Config.OPENWEATHER_API_KEY
        self.base_url = Config.OPENWEATHER_BASE_URL
        self.timeout = 10.0
    
    async def get_weather(self, city: str, country_code: str = "IN") -> Dict[str, Any]:
        """
        Get current weather for a city
        
        Args:
            city: City name (e.g., "Mumbai", "Delhi")
            country_code: ISO 3166 country code (default: "IN" for India)
            
        Returns:
            Dictionary containing weather data or error
        """
        try:
            location = f"{city},{country_code}"
            url = f"{self.base_url}/weather"
            
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
            
            # Parse and structure the weather data
            weather_data = WeatherData(
                location=f"{data['name']}, {data['sys']['country']}",
                temperature=round(data['main']['temp'], 1),
                feels_like=round(data['main']['feels_like'], 1),
                humidity=data['main']['humidity'],
                description=data['weather'][0]['description'].title(),
                wind_speed=round(data['wind']['speed'], 1),
                timestamp=datetime.now().isoformat()
            )
            
            return {
                "success": True,
                "data": weather_data.model_dump(),
                "raw_data": data
            }
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {
                    "success": False,
                    "error": f"City '{city}' not found. Please check spelling.",
                    "error_type": "NOT_FOUND"
                }
            return {
                "success": False,
                "error": f"HTTP error: {e.response.status_code}",
                "error_type": "HTTP_ERROR"
            }
        except httpx.TimeoutException:
            return {
                "success": False,
                "error": "Weather API request timed out",
                "error_type": "TIMEOUT"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "error_type": "UNKNOWN"
            }
    
    async def get_forecast(self, city: str, country_code: str = "IN", days: int = 3) -> Dict[str, Any]:
        """
        Get weather forecast for upcoming days
        
        Args:
            city: City name
            country_code: ISO 3166 country code
            days: Number of days to forecast (max 5)
            
        Returns:
            Dictionary containing forecast data or error
        """
        try:
            location = f"{city},{country_code}"
            url = f"{self.base_url}/forecast"
            
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric",
                "cnt": min(days * 8, 40)  # 8 forecasts per day (3-hour intervals)
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
            
            # Extract daily summaries
            forecasts = []
            for item in data['list'][::8]:  # Get one forecast per day
                forecasts.append({
                    "date": item['dt_txt'].split()[0],
                    "temperature": round(item['main']['temp'], 1),
                    "description": item['weather'][0]['description'].title(),
                    "humidity": item['main']['humidity']
                })
            
            return {
                "success": True,
                "data": {
                    "location": f"{data['city']['name']}, {data['city']['country']}",
                    "forecasts": forecasts[:days]
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Forecast error: {str(e)}",
                "error_type": "FORECAST_ERROR"
            }
