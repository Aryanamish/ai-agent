import os
from typing import Any, Dict, List, Literal

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field


class IntentSchema(BaseModel):
    intent: Literal["greeting", "product_inquiry", "support_request"] = Field(
        description="The classified intent of the user message"
    )

class BotResponse(BaseModel):
    content: str
    intent: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class LLMService:
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            # Try to load from django settings if checking os directly fails, 
            # though os.environ is usually populated by django-environ/python-dotenv
            try:
                from django.conf import settings
                api_key = getattr(settings, "GOOGLE_API_KEY", None)
            except ImportError:
                pass
        
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")

        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=0,
            convert_system_message_to_human=True # Sometimes needed for some models
        )

    def analyze_intent(self, message: str, history: List[BaseMessage] = None) -> IntentSchema:
        structured_llm = self.llm.with_structured_output(IntentSchema)
        
        system_prompt = (
            "You are an intent classifier. Your job is to classify the user's message "
            "into one of the following categories: 'greeting', 'product_inquiry', 'support_request'. "
            "Return ONLY the structured output."
        )
        
        messages = [SystemMessage(content=system_prompt)]
        if history:
             # Just satisfy the type, in real intent classification history might be useful context
             # but keeping it simple for now as per instructions "first identify the intent"
             pass
             
        messages.append(HumanMessage(content=message))
        
        return structured_llm.invoke(messages)

    def generate_chat_response(self, message: str, history: List[BaseMessage], system_instruction: str = "") -> str:
        messages = []
        if system_instruction:
            messages.append(SystemMessage(content=system_instruction))
        
        if history:
            messages.extend(history)
            
        messages.append(HumanMessage(content=message))
        
        response = self.llm.invoke(messages)
        return response.content
