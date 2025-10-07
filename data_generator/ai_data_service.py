"""
AI-powered data generation service using LangChain and LangGraph
"""
import os
import json
import logging
from typing import Dict, List, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
from faker import Faker
import random
from datetime import datetime, date

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = Faker()


class DataGenerationState(TypedDict):
    """State for the data generation workflow"""
    field_name: str
    field_type: str
    ai_description: str
    generated_value: Optional[Any]
    messages: Annotated[List, add_messages]
    error: Optional[str]


class AIDataGenerator:
    """AI-powered data generator using LangChain and LangGraph"""
    
    def __init__(self, openai_api_key: str = None):
        """Initialize the AI data generator"""
        if not openai_api_key:
            # Try to get from Django settings first, then environment
            try:
                from django.conf import settings
                openai_api_key = getattr(settings, 'OPENAI_API_KEY', '')
            except:
                pass
        
        # Fallback to environment variable (using decouple for .env file support)
        if not openai_api_key:
            try:
                from decouple import config
                openai_api_key = config('OPENAI_API_KEY', default='')
            except ImportError:
                openai_api_key = os.getenv('OPENAI_API_KEY', '')
        
        self.openai_api_key = openai_api_key
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY in .env file or pass it directly.")
        
        # Initialize LangChain components
        self.llm = ChatOpenAI(
            api_key=self.openai_api_key,
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        
        # Build the LangGraph workflow
        self.workflow = self._build_workflow()
        
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow for data generation"""
        workflow = StateGraph(DataGenerationState)
        
        # Add nodes
        workflow.add_node("analyze_description", self._analyze_description)
        workflow.add_node("generate_value", self._generate_value)
        workflow.add_node("validate_value", self._validate_value)
        
        # Add edges
        workflow.add_edge("analyze_description", "generate_value")
        workflow.add_edge("generate_value", "validate_value")
        workflow.add_edge("validate_value", END)
        
        # Set entry point
        workflow.set_entry_point("analyze_description")
        
        return workflow.compile()
    
    def _analyze_description(self, state: DataGenerationState) -> DataGenerationState:
        """Analyze the AI description to understand requirements"""
        try:
            system_prompt = """You are an expert data analyst. Analyze the user's description for generating synthetic data.
            Extract key requirements like:
            - Data type and format
            - Ranges (age, dates, numbers)
            - Geographic locations
            - Cultural context
            - Specific patterns or constraints
            - Examples if provided
            
            Respond with a JSON object containing your analysis."""
            
            user_prompt = f"""
            Field name: {state['field_name']}
            Field type: {state['field_type']}
            User description: {state['ai_description']}
            
            Analyze this description and provide structured analysis for generating realistic synthetic data.
            """
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            # Add the analysis to messages for context
            state['messages'] = state.get('messages', []) + [
                {"role": "system", "content": f"Analysis: {response.content}"}
            ]
            
            return state
            
        except Exception as e:
            logger.error(f"Error in analyze_description: {e}")
            state['error'] = str(e)
            return state
    
    def _generate_value(self, state: DataGenerationState) -> DataGenerationState:
        """Generate a value based on the analysis"""
        try:
            field_type = state['field_type']
            ai_description = state['ai_description']
            
            # If there's an error from previous step, use fallback
            if state.get('error'):
                state['generated_value'] = self._fallback_generation(field_type, state['field_name'])
                return state
            
            # Create generation prompt
            system_prompt = f"""You are a synthetic data generator. Generate a single realistic value based on the requirements.
            
            Rules:
            - Generate only the value, no explanations
            - Follow the specified format exactly
            - Consider cultural context if mentioned
            - Use realistic ranges and patterns
            - For {field_type} fields, ensure the output matches the data type
            """
            
            user_prompt = f"""
            Generate a single {field_type} value for field '{state['field_name']}'.
            Requirements: {ai_description}
            
            Return only the generated value.
            """
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            generated_value = response.content.strip()
            
            # Convert to appropriate Python type
            state['generated_value'] = self._convert_to_type(generated_value, field_type)
            
            return state
            
        except Exception as e:
            logger.error(f"Error in generate_value: {e}")
            state['generated_value'] = self._fallback_generation(field_type, state['field_name'])
            return state
    
    def _validate_value(self, state: DataGenerationState) -> DataGenerationState:
        """Validate and potentially adjust the generated value"""
        try:
            value = state['generated_value']
            field_type = state['field_type']
            
            # Basic validation based on field type
            if field_type == 'string' and not isinstance(value, str):
                value = str(value)
            elif field_type == 'number' and not isinstance(value, (int, float)):
                try:
                    value = int(float(str(value).replace(',', '')))
                except:
                    value = random.randint(1, 1000)
            elif field_type == 'decimal' and not isinstance(value, (int, float)):
                try:
                    value = float(str(value).replace(',', ''))
                except:
                    value = round(random.uniform(0, 1000), 2)
            elif field_type == 'boolean':
                if isinstance(value, str):
                    value = value.lower() in ['true', 'yes', '1', 'on']
                else:
                    value = bool(value)
            elif field_type == 'email' and '@' not in str(value):
                value = fake.email()
            elif field_type == 'url' and not str(value).startswith(('http://', 'https://')):
                value = fake.url()
            
            state['generated_value'] = value
            return state
            
        except Exception as e:
            logger.error(f"Error in validate_value: {e}")
            state['generated_value'] = self._fallback_generation(state['field_type'], state['field_name'])
            return state
    
    def _convert_to_type(self, value: str, field_type: str) -> Any:
        """Convert string value to appropriate Python type"""
        try:
            if field_type == 'number':
                return int(float(value.replace(',', '')))
            elif field_type == 'decimal':
                return float(value.replace(',', ''))
            elif field_type == 'boolean':
                return value.lower() in ['true', 'yes', '1', 'on']
            elif field_type == 'date':
                # Try to parse date, fallback to fake date
                try:
                    return datetime.strptime(value, '%Y-%m-%d').date()
                except:
                    return fake.date()
            elif field_type == 'datetime':
                # Try to parse datetime, fallback to fake datetime
                try:
                    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                except:
                    return fake.date_time()
            else:
                return str(value)
        except:
            return self._fallback_generation(field_type, "")
    
    def _fallback_generation(self, field_type: str, field_name: str) -> Any:
        """Fallback data generation using Faker"""
        field_name_lower = field_name.lower()
        
        # Use field name heuristics
        if 'name' in field_name_lower:
            return fake.name()
        elif 'email' in field_name_lower:
            return fake.email()
        elif 'phone' in field_name_lower:
            return fake.phone_number()
        elif 'address' in field_name_lower:
            return fake.address()
        elif 'city' in field_name_lower:
            return fake.city()
        elif 'country' in field_name_lower:
            return fake.country()
        elif 'company' in field_name_lower:
            return fake.company()
        
        # Generate based on field type
        if field_type == 'string':
            return fake.text(max_nb_chars=50)
        elif field_type == 'text':
            return fake.paragraph()
        elif field_type == 'number':
            return random.randint(1, 1000)
        elif field_type == 'decimal':
            return round(random.uniform(0, 1000), 2)
        elif field_type == 'boolean':
            return random.choice([True, False])
        elif field_type == 'date':
            return fake.date()
        elif field_type == 'datetime':
            return fake.date_time()
        elif field_type == 'email':
            return fake.email()
        elif field_type == 'url':
            return fake.url()
        else:
            return fake.word()
    
    def generate_field_value(self, field_name: str, field_type: str, ai_description: str) -> Any:
        """Generate a single field value using AI"""
        if not ai_description or ai_description.strip() == "":
            # No AI description provided, use fallback
            return self._fallback_generation(field_type, field_name)
        
        try:
            # Initialize state
            initial_state = DataGenerationState(
                field_name=field_name,
                field_type=field_type,
                ai_description=ai_description,
                generated_value=None,
                messages=[],
                error=None
            )
            
            # Run the workflow
            result = self.workflow.invoke(initial_state)
            
            return result['generated_value']
            
        except Exception as e:
            logger.error(f"Error generating AI value for {field_name}: {e}")
            return self._fallback_generation(field_type, field_name)
    
    def generate_multiple_values(self, field_definitions: List[Dict], num_records: int = 5) -> List[Dict]:
        """Generate multiple records with AI-enhanced data"""
        data = []
        
        for _ in range(num_records):
            record = {}
            for field_def in field_definitions:
                field_name = field_def['name']
                field_type = field_def['type']
                options = field_def.get('options', {})
                
                # Get AI description
                ai_description = options.get('ai_description', '')
                
                # Handle choice fields separately
                if field_type == 'choice':
                    choices = options.get('choices', ['Option A', 'Option B', 'Option C'])
                    record[field_name] = random.choice(choices)
                elif field_type == 'list':
                    # Generate list as JSON string
                    list_items = [fake.word() for _ in range(random.randint(1, 5))]
                    record[field_name] = json.dumps(list_items)
                else:
                    # Use AI generation
                    record[field_name] = self.generate_field_value(field_name, field_type, ai_description)
            
            data.append(record)
        
        return data


# Global instance holder
_ai_generator = None


def clear_ai_generator_cache():
    """Clear the cached AI generator instance to force reload with new API key"""
    global _ai_generator
    _ai_generator = None


def get_ai_generator(openai_api_key: str = None) -> AIDataGenerator:
    """Get or create AI generator instance"""
    global _ai_generator
    
    if _ai_generator is None or (openai_api_key and openai_api_key != _ai_generator.openai_api_key):
        _ai_generator = AIDataGenerator(openai_api_key)
    
    return _ai_generator


def test_ai_generation():
    """Test function for AI data generation"""
    try:
        generator = get_ai_generator()
        
        # Test data
        test_fields = [
            {
                'name': 'age',
                'type': 'number',
                'options': {'ai_description': 'Ages between 25-40 for working professionals'}
            },
            {
                'name': 'name',
                'type': 'string',
                'options': {'ai_description': 'Names from Latin America, mostly Mexican and Colombian'}
            },
            {
                'name': 'city',
                'type': 'string',
                'options': {'ai_description': 'Cities in Mexico, focus on major metropolitan areas'}
            }
        ]
        
        # Generate test data
        data = generator.generate_multiple_values(test_fields, 5)
        
        print("Generated test data:")
        for i, record in enumerate(data, 1):
            print(f"Record {i}: {record}")
            
        return True
        
    except Exception as e:
        print(f"Test failed: {e}")
        return False


if __name__ == "__main__":
    test_ai_generation()
