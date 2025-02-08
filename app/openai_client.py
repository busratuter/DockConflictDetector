import os
from fastapi import HTTPException
from app.models import ConflictAnalysis
from openai import AzureOpenAI
from dotenv import load_dotenv
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY").strip()
api_version = os.getenv("OPENAI_API_VERSION").strip()
api_base = os.getenv("OPENAI_API_BASE").strip()
deployment_name = os.getenv("OPENAI_DEPLOYMENT_NAME").strip()

http_client = httpx.Client(
    timeout=60.0,  
    verify=False,  
    follow_redirects=True
)

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=api_base,
    timeout=60.0,  
    http_client=http_client,
    max_retries=5  
)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((httpx.ConnectTimeout, httpx.ReadTimeout, ConnectionError, httpx.HTTPError))
)
def analyze_pdf_text(pdf_text: str) -> ConflictAnalysis:
    try:
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
            
        tool_call = completion.choices[0].message.tool_calls[0]
        if tool_call.function.name == "analyze_conflicts":
            import json
            result = json.loads(tool_call.function.arguments)
            return ConflictAnalysis(**result)

        return ConflictAnalysis(conflicts=[])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")