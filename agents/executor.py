"""
Executor Agent - Executes plan steps by calling appropriate tools
"""
import time
from datetime import datetime
from typing import List, Dict, Any
from tools import WeatherTool, NewsTool
from llm.response_models import (
    ExecutorOutput, 
    AgentResponse, 
    AgentType, 
    ToolType,
    PlanStep
)


class ExecutorAgent:
    """
    Executor Agent: Executes plan steps by calling external APIs/tools
    """
    
    def __init__(self):
        """Initialize Executor Agent with tools"""
        self.weather_tool = WeatherTool()
        self.news_tool = NewsTool()
        self.agent_type = AgentType.EXECUTOR
    
    async def execute_plan(self, plan_steps: List[PlanStep]) -> AgentResponse:
        """
        Execute all steps in the plan sequentially
        
        Args:
            plan_steps: List of PlanStep objects from Planner
            
        Returns:
            AgentResponse containing list of ExecutorOutput
        """
        try:
            executor_outputs = []
            
            for step in plan_steps:
                output = await self._execute_single_step(step)
                executor_outputs.append(output)
            
            # Calculate success rate
            successful_steps = sum(1 for out in executor_outputs if out.success)
            success_rate = successful_steps / len(executor_outputs) if executor_outputs else 0
            
            return AgentResponse(
                agent_type=self.agent_type,
                success=success_rate > 0.5,  # At least 50% steps should succeed
                message=f"Executed {len(executor_outputs)} steps ({successful_steps} successful)",
                data={
                    "executor_outputs": [out.model_dump() for out in executor_outputs],
                    "success_rate": round(success_rate, 2)
                },
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            return AgentResponse(
                agent_type=self.agent_type,
                success=False,
                message="Failed to execute plan",
                error=str(e),
                timestamp=datetime.now().isoformat()
            )
    
    async def _execute_single_step(self, step: PlanStep) -> ExecutorOutput:
        """
        Execute a single plan step
        
        Args:
            step: PlanStep to execute
            
        Returns:
            ExecutorOutput with results
        """
        start_time = time.time()
        
        try:
            if step.tool_required == ToolType.WEATHER:
                result = await self._call_weather_tool(step.parameters)
            elif step.tool_required == ToolType.NEWS:
                result = await self._call_news_tool(step.parameters)
            else:
                result = {
                    "success": False,
                    "error": f"Unknown tool: {step.tool_required}"
                }
            
            execution_time = time.time() - start_time
            
            return ExecutorOutput(
                step_number=step.step_number,
                tool_used=step.tool_required,
                success=result.get("success", False),
                data=result.get("data", {}),
                error_message=result.get("error"),
                execution_time=round(execution_time, 2)
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutorOutput(
                step_number=step.step_number,
                tool_used=step.tool_required,
                success=False,
                data={},
                error_message=str(e),
                execution_time=round(execution_time, 2)
            )
    
    async def _call_weather_tool(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call weather API tool
        
        Args:
            parameters: Dictionary with 'city' and optional 'country_code'
            
        Returns:
            Weather data result
        """
        city = parameters.get("city", "Mumbai")
        country_code = parameters.get("country_code", "IN")
        
        # Check if forecast is requested
        if parameters.get("forecast", False):
            days = parameters.get("days", 3)
            return await self.weather_tool.get_forecast(city, country_code, days)
        else:
            return await self.weather_tool.get_weather(city, country_code)
    
    async def _call_news_tool(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call news API tool
        
        Args:
            parameters: Dictionary with 'query' or 'category'
            
        Returns:
            News data result
        """
        query = parameters.get("query")
        category = parameters.get("category")
        country = parameters.get("country", "in")
        limit = parameters.get("limit", 5)
        
        if query:
            return await self.news_tool.get_news(query, country=country, limit=limit)
        elif category:
            return await self.news_tool.get_top_headlines(category, country=country, limit=limit)
        else:
            # Default: get general top headlines
            return await self.news_tool.get_top_headlines(country=country, limit=limit)
