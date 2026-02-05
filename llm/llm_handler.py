"""
LLM Handler for Google Gemini with structured output support
"""
import json
import google.generativeai as genai
from typing import Type, TypeVar, Optional
from pydantic import BaseModel
from .config import Config

T = TypeVar('T', bound=BaseModel)


class LLMHandler:
    """Handler for Google Gemini API with structured output generation"""
    
    def __init__(self):
        """Initialize Gemini API"""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=Config.GEMINI_MODEL,
            generation_config={
                "temperature": Config.TEMPERATURE,
                "max_output_tokens": Config.MAX_TOKENS,
            }
        )
    
    def generate_structured_output(
        self,
        prompt: str,
        output_model: Type[T],
        system_instruction: Optional[str] = None
    ) -> T:
        """
        Generate structured output conforming to Pydantic model
        
        Args:
            prompt: User prompt
            output_model: Pydantic model for output structure
            system_instruction: Optional system instruction
            
        Returns:
            Validated instance of output_model
        """
        try:
            schema = output_model.model_json_schema()
            
            full_prompt = f"""
{system_instruction if system_instruction else ''}

User Request: {prompt}

Respond with VALID JSON matching this schema:
{json.dumps(schema, indent=2)}

Requirements:
- Output ONLY valid JSON
- No markdown, no explanations
- Include all required fields
- Match data types exactly

JSON Response:
"""
            
            response = self.model.generate_content(full_prompt)
            response_text = response.text.strip()
            
            # Clean markdown if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            # Parse and validate
            parsed_data = json.loads(response_text)
            validated_output = output_model(**parsed_data)
            
            return validated_output
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {e}\nResponse: {response_text}")
        except Exception as e:
            raise RuntimeError(f"Error generating output: {e}")
    
    def generate_text(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Generate simple text response"""
        try:
            full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt
            response = self.model.generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            raise RuntimeError(f"Error generating text: {e}")
