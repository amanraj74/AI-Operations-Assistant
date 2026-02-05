"""
Pydantic models for structured LLM outputs and API responses
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class AgentType(str, Enum):
    """Types of agents in the system"""
    PLANNER = "planner"
    EXECUTOR = "executor"
    VERIFIER = "verifier"


class ToolType(str, Enum):
    """Available tools for execution"""
    WEATHER = "weather"
    NEWS = "news"
    NONE = "none"


class PlanStep(BaseModel):
    """Single step in the execution plan"""
    step_number: int = Field(..., description="Sequential step number")
    description: str = Field(..., description="What needs to be done")
    tool_required: ToolType = Field(..., description="Which tool to use")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Parameters for the tool")


class PlannerOutput(BaseModel):
    """Structured output from Planner Agent"""
    user_intent: str = Field(..., description="Clear understanding of user's request")
    plan_steps: List[PlanStep] = Field(..., description="List of steps to execute")
    estimated_complexity: str = Field(..., description="Simple/Medium/Complex")
    reasoning: str = Field(..., description="Why this plan was chosen")


class WeatherData(BaseModel):
    """Weather information structure"""
    location: str
    temperature: float
    feels_like: float
    humidity: int
    description: str
    wind_speed: float
    timestamp: str


class NewsArticle(BaseModel):
    """News article structure"""
    title: str
    description: Optional[str] = None
    url: str
    published_at: str
    source: str


class ExecutorOutput(BaseModel):
    """Structured output from Executor Agent"""
    step_number: int
    tool_used: ToolType
    success: bool
    data: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    execution_time: float


class VerificationStatus(str, Enum):
    """Verification result status"""
    APPROVED = "approved"
    NEEDS_RETRY = "needs_retry"
    FAILED = "failed"


class VerifierOutput(BaseModel):
    """Structured output from Verifier Agent"""
    status: VerificationStatus
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence in verification (0-1)")
    issues_found: List[str] = Field(default_factory=list, description="List of issues if any")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    final_response: str = Field(..., description="Formatted response for user")


class AgentResponse(BaseModel):
    """Unified response structure for all agents"""
    agent_type: AgentType
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str


class FinalOutput(BaseModel):
    """Complete system output"""
    request_id: str
    user_query: str
    planner_output: Optional[PlannerOutput] = None
    executor_outputs: List[ExecutorOutput] = Field(default_factory=list)
    verifier_output: Optional[VerifierOutput] = None
    final_response: str
    total_execution_time: float
    success: bool
