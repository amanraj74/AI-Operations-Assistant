"""
Planner Agent - Analyzes user request and creates execution plan
"""
import time
from datetime import datetime
from llm.llm_handler import LLMHandler
from llm.response_models import PlannerOutput, AgentResponse, AgentType


class PlannerAgent:
    """
    Planner Agent: Understands user intent and creates a structured execution plan
    """
    
    def __init__(self):
        """Initialize Planner Agent with LLM handler"""
        self.llm = LLMHandler()
        self.agent_type = AgentType.PLANNER
    
    async def create_plan(self, user_query: str) -> AgentResponse:
        """
        Analyze user query and create a structured execution plan
        
        Args:
            user_query: The user's natural language request
            
        Returns:
            AgentResponse containing PlannerOutput
        """
        try:
            start_time = time.time()
            
            system_instruction = """
You are a Planner Agent in a multi-agent system for TrulyMadly dating app.
Your role is to understand user requests and create actionable execution plans.

Available Tools:
1. weather - Get weather information for any city
2. news - Get news articles, events, or headlines

Context: Users often ask about planning dates, outings, events, or getting information about places.

Your task:
- Understand the user's true intent
- Break down the request into logical steps
- Assign appropriate tools to each step
- Provide clear parameters for each tool call

Examples of user intents:
- "Plan a date in Mumbai" → Need weather + local events/news
- "What's the weather in Delhi?" → Need weather only
- "Latest tech news" → Need news only
- "Weekend outing in Bangalore" → Need weather + entertainment news
"""
            
            planner_output = self.llm.generate_structured_output(
                prompt=user_query,
                output_model=PlannerOutput,
                system_instruction=system_instruction
            )
            
            execution_time = time.time() - start_time
            
            return AgentResponse(
                agent_type=self.agent_type,
                success=True,
                message=f"Plan created with {len(planner_output.plan_steps)} steps",
                data={
                    "planner_output": planner_output.model_dump(),
                    "execution_time": round(execution_time, 2)
                },
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            return AgentResponse(
                agent_type=self.agent_type,
                success=False,
                message="Failed to create plan",
                error=str(e),
                timestamp=datetime.now().isoformat()
            )
    
    def extract_location(self, query: str) -> str:
        """
        Extract city/location from user query
        
        Args:
            query: User query text
            
        Returns:
            Extracted city name or default "Mumbai"
        """
        # Common Indian cities
        cities = [
            "mumbai", "delhi", "bangalore", "hyderabad", "chennai",
            "kolkata", "pune", "ahmedabad", "jaipur", "surat",
            "lucknow", "kanpur", "nagpur", "indore", "bhopal",
            "patna", "vadodara", "ghaziabad", "ludhiana", "agra"
        ]
        
        query_lower = query.lower()
        for city in cities:
            if city in query_lower:
                return city.title()
        
        return "Mumbai"  # Default city
