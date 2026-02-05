"""
Verifier Agent - Validates execution results and formats final response
"""
import time
from datetime import datetime
from typing import List, Dict, Any
from llm.llm_handler import LLMHandler
from llm.response_models import (
    VerifierOutput,
    AgentResponse,
    AgentType,
    ExecutorOutput,
    PlannerOutput
)


class VerifierAgent:
    """
    Verifier Agent: Validates results and creates user-friendly responses
    """
    
    def __init__(self):
        """Initialize Verifier Agent with LLM handler"""
        self.llm = LLMHandler()
        self.agent_type = AgentType.VERIFIER
    
    async def verify_and_format(
        self,
        user_query: str,
        planner_output: PlannerOutput,
        executor_outputs: List[ExecutorOutput]
    ) -> AgentResponse:
        """
        Verify execution results and create final formatted response
        
        Args:
            user_query: Original user query
            planner_output: Output from Planner Agent
            executor_outputs: List of outputs from Executor Agent
            
        Returns:
            AgentResponse containing VerifierOutput
        """
        try:
            start_time = time.time()
            
            # Analyze execution results
            analysis = self._analyze_results(executor_outputs)
            
            # Generate verification using LLM
            system_instruction = """
You are a Verifier Agent for TrulyMadly dating app's multi-agent system.
Your role is to:
1. Check if the execution results answer the user's question
2. Identify any issues or missing information
3. Create a natural, helpful response for the user
4. Provide a confidence score (0.0 to 1.0)

Guidelines:
- Be conversational and friendly (dating app context)
- If weather data exists, mention temperature, conditions, and recommendations
- If news/events exist, highlight interesting articles
- If data is missing, acknowledge it politely
- Format the response in a clear, engaging way
"""
            
            verification_prompt = f"""
User Query: {user_query}

Planned Intent: {planner_output.user_intent}

Execution Results:
{self._format_execution_data(executor_outputs)}

Analysis:
- Total steps: {len(executor_outputs)}
- Successful: {analysis['successful_count']}
- Failed: {analysis['failed_count']}

Based on this, verify the quality and create a final response for the user.
"""
            
            verifier_output = self.llm.generate_structured_output(
                prompt=verification_prompt,
                output_model=VerifierOutput,
                system_instruction=system_instruction
            )
            
            execution_time = time.time() - start_time
            
            return AgentResponse(
                agent_type=self.agent_type,
                success=True,
                message="Verification complete",
                data={
                    "verifier_output": verifier_output.model_dump(),
                    "execution_time": round(execution_time, 2)
                },
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            # Fallback: create basic response without LLM
            fallback_response = self._create_fallback_response(user_query, executor_outputs)
            
            return AgentResponse(
                agent_type=self.agent_type,
                success=True,
                message="Verification complete (fallback mode)",
                data={
                    "verifier_output": fallback_response,
                    "execution_time": 0
                },
                error=f"LLM verification failed: {str(e)}",
                timestamp=datetime.now().isoformat()
            )
    
    def _analyze_results(self, executor_outputs: List[ExecutorOutput]) -> Dict[str, Any]:
        """Analyze executor outputs for quality metrics"""
        successful = [out for out in executor_outputs if out.success]
        failed = [out for out in executor_outputs if not out.success]
        
        return {
            "total_count": len(executor_outputs),
            "successful_count": len(successful),
            "failed_count": len(failed),
            "success_rate": len(successful) / len(executor_outputs) if executor_outputs else 0,
            "has_weather": any(out.tool_used.value == "weather" and out.success for out in executor_outputs),
            "has_news": any(out.tool_used.value == "news" and out.success for out in executor_outputs)
        }
    
    def _format_execution_data(self, executor_outputs: List[ExecutorOutput]) -> str:
        """Format execution data for LLM prompt"""
        formatted = []
        
        for output in executor_outputs:
            status = "✓ SUCCESS" if output.success else "✗ FAILED"
            formatted.append(f"Step {output.step_number} ({output.tool_used.value}): {status}")
            
            if output.success and output.data:
                formatted.append(f"  Data: {str(output.data)[:200]}...")
            elif output.error_message:
                formatted.append(f"  Error: {output.error_message}")
        
        return "\n".join(formatted)
    
    def _create_fallback_response(
        self,
        user_query: str,
        executor_outputs: List[ExecutorOutput]
    ) -> Dict[str, Any]:
        """Create a basic response when LLM verification fails"""
        from llm.response_models import VerificationStatus
        
        successful_outputs = [out for out in executor_outputs if out.success]
        
        if not successful_outputs:
            return {
                "status": VerificationStatus.FAILED,
                "confidence_score": 0.0,
                "issues_found": ["All execution steps failed"],
                "suggestions": ["Check API keys", "Verify network connection"],
                "final_response": "I apologize, but I couldn't fetch the required information at this moment. Please try again later."
            }
        
        # Build simple response from data
        response_parts = []
        for output in successful_outputs:
            if output.tool_used.value == "weather" and output.data:
                weather = output.data.get("data", {})
                response_parts.append(
                    f"Weather: {weather.get('temperature')}°C, {weather.get('description')}"
                )
            elif output.tool_used.value == "news" and output.data:
                news = output.data.get("data", {})
                response_parts.append(
                    f"Found {news.get('total_results', 0)} news articles"
                )
        
        return {
            "status": VerificationStatus.APPROVED,
            "confidence_score": 0.7,
            "issues_found": [],
            "suggestions": [],
            "final_response": " | ".join(response_parts) if response_parts else "Information retrieved successfully."
        }
