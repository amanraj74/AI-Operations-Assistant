"""
AI Operations Assistant - Multi-Agent System
FastAPI application orchestrating Planner, Executor, and Verifier agents
"""
import time
import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from llm.config import Config
from agents import PlannerAgent, ExecutorAgent, VerifierAgent
from llm.response_models import FinalOutput, PlanStep, PlannerOutput, ExecutorOutput


# Initialize FastAPI
app = FastAPI(
    title=Config.APP_NAME,
    version=Config.APP_VERSION,
    description="Multi-agent AI system for intelligent task execution with real-time API integration"
)


class QueryRequest(BaseModel):
    """User query request model"""
    query: str = Field(..., min_length=3, max_length=500)


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    app_name: str
    version: str
    timestamp: str


# Agent instances
planner_agent = None
executor_agent = None
verifier_agent = None


@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    global planner_agent, executor_agent, verifier_agent
    
    try:
        Config.validate()
        
        planner_agent = PlannerAgent()
        executor_agent = ExecutorAgent()
        verifier_agent = VerifierAgent()
        
        print("=" * 70)
        print(f"🚀 {Config.APP_NAME} v{Config.APP_VERSION}")
        print("✓ Multi-agent system initialized")
        print("✓ API keys validated")
        print("✓ Ready to process queries")
        print("=" * 70)
        
    except ValueError as e:
        print("=" * 70)
        print(f"✗ Configuration Error: {e}")
        print("✗ Update .env file with valid API keys")
        print("=" * 70)
        raise
    except Exception as e:
        print("=" * 70)
        print(f"✗ Startup Error: {e}")
        print("=" * 70)
        raise


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint"""
    return HealthResponse(
        status="healthy",
        app_name=Config.APP_NAME,
        version=Config.APP_VERSION,
        timestamp=datetime.now().isoformat()
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        app_name=Config.APP_NAME,
        version=Config.APP_VERSION,
        timestamp=datetime.now().isoformat()
    )


@app.post("/query", response_model=FinalOutput)
async def process_query(request: QueryRequest):
    """
    Main endpoint: Process natural language query through multi-agent system
    
    Architecture Flow:
    1. Planner Agent: Analyzes query and creates execution plan
    2. Executor Agent: Executes plan steps with API calls
    3. Verifier Agent: Validates results and formats response
    """
    start_time = time.time()
    request_id = str(uuid.uuid4())[:8]
    
    try:
        # STEP 1: Planner
        print(f"\n[{request_id}] 🧠 PLANNER: Analyzing query...")
        planner_response = await planner_agent.create_plan(request.query)
        
        if not planner_response.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Planner failed: {planner_response.error}"
            )
        
        planner_output_dict = planner_response.data["planner_output"]
        print(f"[{request_id}] ✓ Created plan with {len(planner_output_dict['plan_steps'])} steps")
        
        # STEP 2: Executor
        print(f"[{request_id}] ⚙️  EXECUTOR: Executing plan...")
        plan_steps = [PlanStep(**step) for step in planner_output_dict["plan_steps"]]
        executor_response = await executor_agent.execute_plan(plan_steps)
        
        if not executor_response.success:
            print(f"[{request_id}] ⚠️  Warning: Some steps failed")
        else:
            print(f"[{request_id}] ✓ Execution complete")
        
        executor_outputs_dict = executor_response.data["executor_outputs"]
        
        # STEP 3: Verifier
        print(f"[{request_id}] 🔍 VERIFIER: Validating results...")
        planner_output = PlannerOutput(**planner_output_dict)
        executor_outputs = [ExecutorOutput(**out) for out in executor_outputs_dict]
        
        verifier_response = await verifier_agent.verify_and_format(
            user_query=request.query,
            planner_output=planner_output,
            executor_outputs=executor_outputs
        )
        
        if not verifier_response.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Verifier failed: {verifier_response.error}"
            )
        
        verifier_output_dict = verifier_response.data["verifier_output"]
        print(f"[{request_id}] ✓ Verification complete")
        
        total_time = time.time() - start_time
        
        # Build final output
        final_output = FinalOutput(
            request_id=request_id,
            user_query=request.query,
            planner_output=planner_output,
            executor_outputs=executor_outputs,
            verifier_output=verifier_output_dict,
            final_response=verifier_output_dict["final_response"],
            total_execution_time=round(total_time, 2),
            success=verifier_output_dict["status"] == "approved"
        )
        
        print(f"[{request_id}] ✅ Completed in {total_time:.2f}s\n")
        
        return final_output
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[{request_id}] ✗ Error: {str(e)}\n")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Processing error: {str(e)}"
        )


@app.get("/examples")
async def get_examples():
    """Get example queries for testing"""
    return {
        "examples": [
            {
                "query": "Plan a date in Mumbai this weekend",
                "tools": ["weather", "news"]
            },
            {
                "query": "What's the weather in Bangalore?",
                "tools": ["weather"]
            },
            {
                "query": "Latest tech news in India",
                "tools": ["news"]
            },
            {
                "query": "Outdoor activity suggestions for Delhi",
                "tools": ["weather", "news"]
            },
            {
                "query": "Check Goa weather and local events",
                "tools": ["weather", "news"]
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=Config.DEBUG)
