import os
from fastapi import HTTPException
from app.models import ConflictAnalysis, Conflict
from openai import AzureOpenAI
from dotenv import load_dotenv
import openai

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY").strip()
api_version = os.getenv("OPENAI_API_VERSION").strip()
api_base = os.getenv("OPENAI_API_BASE").strip()
deployment_name = os.getenv("OPENAI_DEPLOYMENT_NAME").strip()

print(f"API Base: {api_base}")
print(f"API Version: {api_version}")
print(f"Deployment: {deployment_name}")

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=api_base
)

def analyze_pdf_text(pdf_text: str) -> ConflictAnalysis:
    try:
        print(f"Using deployment: {deployment_name}")
        print(f"PDF text length: {len(pdf_text)}")

        tools = [{
            "type": "function",
            "function": {
                "name": "analyze_conflicts",
                "description": "Analyze conflicts in the given text",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "conflicts": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "section1": {"type": "string"},
                                    "section2": {"type": "string"},
                                    "conflict_description": {"type": "string"}
                                },
                                "required": ["section1", "section2", "conflict_description"]
                            }
                        }
                    },
                    "required": ["conflicts"]
                }
            }
        }]

        print("Making API request...")
        completion = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert in language analysis. Analyze the text and identify conflicting statements using the provided function."
                },
                {
                    "role": "user", 
                    "content": "Analyze the following text and identify any conflicting statements:\n\n" + pdf_text
                }
            ],
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "analyze_conflicts"}}
        )
        print("API request completed")
            
        tool_call = completion.choices[0].message.tool_calls[0]
        if tool_call.function.name == "analyze_conflicts":
            import json
            result = json.loads(tool_call.function.arguments)
            return ConflictAnalysis(**result)

        return ConflictAnalysis(conflicts=[])

    except Exception as e:
        print(f"Hata detayı: {str(e)}")
        print(f"Deployment name: {deployment_name}")
        print(f"API Version: {api_version}")
        print(f"API Base: {api_base}")
        if hasattr(e, 'response'):
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        raise HTTPException(status_code=500, detail=f"OpenAI API hatası: {str(e)}")