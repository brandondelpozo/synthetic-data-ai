# AI-Enhanced Synthetic Data Generation

## Overview

This Dynamic Model Builder now includes AI-powered data generation using LangChain and LangGraph. Users can provide detailed descriptions for each field, and the system will use OpenAI's GPT models to generate more accurate and contextually appropriate synthetic data.

## New Features

### 1. Removed Display Name Field
- The "Display Name" input field has been removed from the model builder form
- Display names are now automatically generated from the table name

### 2. AI Description Field
- Replaced "Faker Type" dropdown with "Description for AI" textarea
- Users can provide detailed descriptions like:
  - "Ages between 18-65 for working professionals"
  - "Names from Latin America, mostly Mexican and Colombian"
  - "Cities in Mexico, focus on major metropolitan areas"
  - "Phone numbers in international format from European countries"

### 3. AI-Powered Data Generation
- Uses LangChain and LangGraph for intelligent data processing
- Implements a workflow that:
  1. Analyzes the user's description
  2. Generates appropriate synthetic data
  3. Validates and converts the data to proper types
- Falls back to traditional Faker generation if AI fails or no description is provided

### 4. OpenAI Integration
- Users provide their OpenAI API key when generating data
- Uses GPT-3.5-turbo for cost-effective generation
- API key is only used during data generation and not stored

## How to Use

### Setting Up
1. Get your OpenAI API key from https://platform.openai.com/api-keys
2. Install dependencies: `pip install -r requirements.txt`

### Creating Tables with AI Descriptions
1. Navigate to the Model Builder
2. Enter a table name (e.g., "user_profiles")
3. Add fields with detailed AI descriptions:
   - Field Name: `age`
   - Data Type: `number`
   - Description for AI: `Ages between 25-40 for working professionals`

### Generating Data
1. Go to your table's detail page
2. Enter the number of records to generate
3. **Provide your OpenAI API key** in the designated field
4. Click "Generate & Export Excel"

The system will use AI for fields with descriptions and fall back to standard generation for others.

## Technical Implementation

### Architecture
- `ai_data_service.py`: Main AI service using LangChain/LangGraph
- `dynamic_models.py`: Modified to integrate AI generation
- `views.py`: Updated to handle AI descriptions and API keys

### Workflow (LangGraph)
```
1. analyze_description → Analyzes user requirements
2. generate_value → Creates synthetic data based on analysis  
3. validate_value → Ensures data type compliance
```

### Dependencies Added
- `langchain==0.3.14`
- `langchain-openai==0.2.14` 
- `langgraph==0.2.51`
- `openai==1.58.1`

## Examples

### Example 1: Professional User Data
```
Field: first_name
Type: string  
Description: "First names common in Latin America, particularly Mexico and Colombia"

Field: age
Type: number
Description: "Ages between 25-45 for working professionals"

Field: salary
Type: decimal
Description: "Annual salaries in USD for mid-level professionals, range 45000-85000"
```

### Example 2: Product Catalog
```
Field: product_name
Type: string
Description: "Electronic product names for smartphones and tablets, modern brands"

Field: price
Type: decimal  
Description: "Prices in USD for consumer electronics, range 200-1500"

Field: country_origin
Type: string
Description: "Manufacturing countries, focus on Asian markets like China, South Korea, Japan"
```

## Error Handling

- If OpenAI API key is invalid or missing, standard Faker generation is used
- If AI generation fails for any field, it falls back to traditional methods
- All errors are logged and the system continues gracefully

## Cost Considerations

- Uses GPT-3.5-turbo for cost efficiency
- Each field description generates one API call per record
- Approximate cost: $0.001-0.002 per 100 records with AI descriptions
- Users only pay for what they use (their own API key)

## Security

- OpenAI API keys are not stored in the database
- Keys are only used during the generation request
- All AI communication is handled securely through official OpenAI client

## Future Enhancements

- Support for more AI models (GPT-4, Claude, etc.)
- Batch generation optimization
- AI-powered validation and quality checks
- Custom AI prompts and templates
- Integration with other LLM providers
