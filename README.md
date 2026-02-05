# AI Operations Assistant

> **Multi-Agent System for Intelligent Query Processing**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A production-ready multi-agent AI system that processes natural language queries through intelligent planning, execution, and verification. Built with FastAPI, Google Gemini, and real-time API integrations for weather data and news content.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Example Usage](#example-usage)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

### What This System Does

The AI Operations Assistant accepts natural language queries, intelligently plans execution steps, calls real-world APIs, and returns structured, contextual responses.

**Example Flow:**

```
User Query: "Plan a romantic date in Mumbai this weekend"

System Process:
1. Planner Agent (LLM) → Analyzes intent: needs weather + local events
2. Executor Agent (APIs) → Fetches real-time weather data + news/events
3. Verifier Agent (LLM) → Validates results + formats natural response

Output:
"Weather in Mumbai: 32°C with clear skies. Perfect for outdoor activities! 
Here are 3 exciting events this weekend: [Concert at Marine Drive], 
[Food Festival at Bandra]..."
```

### Key Features

- ✅ **Multi-Agent Architecture** - Planner, Executor, and Verifier agents with clear separation of concerns
- ✅ **Structured LLM Outputs** - Type-safe responses using Google Gemini and Pydantic schemas
- ✅ **Real API Integration** - OpenWeatherMap and TheNewsAPI for live data
- ✅ **Async Operations** - Non-blocking API calls for improved performance
- ✅ **Interactive Documentation** - Built-in Swagger UI and ReDoc
- ✅ **Error Handling** - Graceful failures with user-friendly messages
- ✅ **Type Safety** - Full type hints throughout the codebase

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      User Query                         │
│                (Natural Language Input)                 │
└────────────────────┬────────────────────────────────────┘
                     ↓
         ┌───────────────────────┐
         │   PLANNER AGENT       │
         │   (Google Gemini)     │
         │                       │
         │ - Understand intent   │
         │ - Create step plan    │
         │ - Select tools        │
         └──────────┬────────────┘
                    ↓
         ┌───────────────────────┐
         │   EXECUTOR AGENT      │
         │   (API Caller)        │
         │                       │
         │ - Call Weather API    │
         │ - Call News API       │
         │ - Handle errors       │
         └──────────┬────────────┘
                    ↓
         ┌───────────────────────┐
         │   VERIFIER AGENT      │
         │   (Google Gemini)     │
         │                       │
         │ - Validate results    │
         │ - Check completeness  │
         │ - Format response     │
         └──────────┬────────────┘
                    ↓
         ┌───────────────────────┐
         │    Final Response     │
         │      (JSON + Text)    │
         └───────────────────────┘
```

### Agent Responsibilities

| Agent | Purpose | Technology | Output |
|-------|---------|------------|--------|
| **Planner** | Intent analysis, execution planning | Google Gemini LLM | JSON plan with steps and tools |
| **Executor** | API calls, data retrieval | HTTP clients | Structured data from APIs |
| **Verifier** | Quality validation, response formatting | Google Gemini LLM | User-friendly final response |

---

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Internet connection for API calls
- Free API keys (see setup instructions below)

### Installation

```bash
# Clone the repository
git clone https://github.com/amanraj74/AI-Operations-Assistant.git
cd AI-Operations-Assistant

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### API Keys Setup

**Step 1: Obtain Free API Keys**

1. **Google Gemini API** (Free, 1 minute setup)
   - Visit: https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy the key

2. **OpenWeatherMap API** (Free, 1000 calls/day)
   - Visit: https://openweathermap.org/api
   - Sign up for free account
   - Get API key from: https://home.openweathermap.org/api_keys

3. **TheNewsAPI** (Free, 150 requests/day)
   - Visit: https://www.thenewsapi.com/
   - Sign up for free account
   - Copy your API key

**Step 2: Configure Environment Variables**

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your actual API keys
```

Your `.env` file should look like:

```env
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXX
OPENWEATHER_API_KEY=3d6c55f18XXXXXXXXXXXXXXXXXX
NEWS_API_KEY=u9Rs9TYvKXXXXXXXXXXXXXXXXXXXXX

APP_NAME=AI Operations Assistant
APP_VERSION=1.0.0
DEBUG=True
```

### Running the Application

```bash
uvicorn main:app --reload
```

**Expected Output:**

```
======================================================================
🚀 AI Operations Assistant v1.0.0
✓ Multi-agent system initialized
✓ API keys validated
✓ Ready to process queries
======================================================================
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Application URLs:**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

---

## API Documentation

### Endpoints

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-05T10:30:00Z"
}
```

#### Process Query
```http
POST /query
Content-Type: application/json
```

**Request Body:**
```json
{
  "query": "What's the weather in Mumbai?"
}
```

**Response:**
```json
{
  "query": "What's the weather in Mumbai?",
  "plan": {
    "user_intent": "Get weather information for Mumbai",
    "plan_steps": [...],
    "estimated_complexity": "simple"
  },
  "execution_results": {...},
  "final_response": "The current weather in Mumbai is 32°C with clear skies...",
  "processing_time": "4.52s"
}
```

#### Get Examples
```http
GET /examples
```

Returns a list of example queries to test the system.

---

## Example Usage

### Browser (Easiest Method)

1. Open browser: http://localhost:8000/docs
2. Click on **POST /query**
3. Click "Try it out"
4. Paste example query:
   ```json
   {
     "query": "What's the weather in Mumbai?"
   }
   ```
5. Click "Execute"
6. View the complete agent flow and response

### Command Line (cURL)

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the weather in Mumbai?"}'
```

### Python Script

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={"query": "Plan a date in Delhi this weekend"}
)

print(response.json()["final_response"])
```

### Example Prompts

**Single Tool Queries:**
- `"What's the weather in Patna?"`
- `"Show me latest technology news in India"`
- `"How hot is it in Bangalore right now?"`

**Multi-Tool Queries:**
- `"Plan a romantic date in Mumbai this weekend"`
- `"Should I do outdoor activities in Delhi today?"`
- `"Check Goa weather and local events"`

---

## Technology Stack

### Core Framework
- **FastAPI** - Modern async web framework
- **Pydantic** - Data validation and structured outputs
- **Python 3.10** - Type hints and async support

### LLM Integration
- **Google Gemini** (gemini-2.5-flash) - Natural language understanding
- **Structured Output Generation** - JSON schema-constrained responses

### External APIs
- **OpenWeatherMap** - Real-time weather data
- **TheNewsAPI** - News articles and events

---

## Project Structure

```
ai_ops_assistant/
├── agents/
│   ├── __init__.py
│   ├── planner.py              # Planner Agent: Intent → Plan
│   ├── executor.py             # Executor Agent: Plan → API Calls
│   └── verifier.py             # Verifier Agent: Validation → Response
├── tools/
│   ├── __init__.py
│   ├── weather_tool.py         # OpenWeatherMap wrapper
│   └── news_tool.py            # TheNewsAPI wrapper
├── llm/
│   ├── __init__.py
│   ├── config.py               # Configuration management
│   ├── llm_handler.py          # Gemini API handler
│   └── response_models.py      # Pydantic schemas
├── main.py                      # FastAPI application (entry point)
├── requirements.txt             # Python dependencies
├── .env                         # API keys (gitignored)
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

### Key Files

- **main.py** - FastAPI application orchestrating all agents
- **agents/planner.py** - Converts queries into JSON execution plans
- **agents/executor.py** - Executes plans by calling weather/news APIs
- **agents/verifier.py** - Validates results and formats responses
- **llm/llm_handler.py** - Wrapper for Gemini API with structured outputs
- **llm/response_models.py** - Pydantic models ensuring type-safe LLM outputs

---

## Configuration

### Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `GEMINI_API_KEY` | Google Gemini API access | Yes |
| `OPENWEATHER_API_KEY` | Weather data access | Yes |
| `NEWS_API_KEY` | News data access | Yes |
| `DEBUG` | Enable debug mode | No (default: True) |

### LLM Settings

Edit `llm/config.py` to customize:
- `GEMINI_MODEL` - Model version
- `TEMPERATURE` - Response creativity (0.0-1.0)
- `MAX_TOKENS` - Maximum response length

---

## Troubleshooting

### Server Won't Start

**Error:** `ValueError: Missing required API keys`

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Verify keys are set (not placeholder values)
cat .env

# Ensure no extra spaces around = signs
# Correct:   GEMINI_API_KEY=abc123
# Incorrect: GEMINI_API_KEY = abc123
```

### API Calls Failing

**Error:** `HTTP 401 Unauthorized`

**Solution:** Verify API keys are active and correct. Check API dashboard for any restrictions.

### Slow Responses

**Issue:** Queries taking >15 seconds

**Possible Causes:**
- Slow internet connection
- API rate limiting (429 errors)
- LLM server latency

**Solutions:**
- Check internet speed
- Wait a few minutes if hitting rate limits
- Try simpler single-tool queries first

### 422 Unprocessable Entity

**Error:** JSON decode error in API request

**Solution:**
```bash
# Ensure valid JSON format
# Use double quotes, not single quotes
# Correct:   {"query": "test"}
# Incorrect: {'query': 'test'}
```

---

## Known Limitations

1. **Sequential Execution** - Steps execute one after another (average 5-7 seconds per query)
2. **API Rate Limits** - Free tier limits (1000/day weather, 150/day news)
3. **News API Coverage** - Limited sources in free tier, some queries may return 0 results
4. **City Name Ambiguity** - Default country code is "IN" for India context

---

## Future Improvements

**With More Time:**
- Implement response caching (Redis)
- Parallel tool execution (asyncio.gather)
- Stream LLM responses to reduce perceived latency
- Add restaurant/place recommendations API
- Integrate maps/directions API
- User preference storage and context
- Cost tracking and analytics dashboard

---

## License

This project is submitted as part of the TrulyMadly GenAI Intern Assignment (24-Hour Challenge) - February 2026.

---

## Author

**Name:** Aman Raj  
**GitHub:** [@amanraj74](https://github.com/amanraj74)  
**Repository:** [AI-Operations-Assistant](https://github.com/amanraj74/AI-Operations-Assistant)  
**Submission Date:** February 5, 2026  
**Assignment:** 24-Hour GenAI Intern Technical Assessment

---

## Acknowledgments

- Google Gemini for powerful LLM capabilities
- OpenWeatherMap for reliable weather data
- TheNewsAPI for news aggregation
- FastAPI for the excellent async web framework
- Pydantic for data validation and structured outputs