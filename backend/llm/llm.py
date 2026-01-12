import os
from typing import Any, Dict, List, Literal

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from pydantic import BaseModel, Field

# Try imports for different providers
try:
    from langchain_google_genai import (
        ChatGoogleGenerativeAI,
        GoogleGenerativeAIEmbeddings,
    )
except ImportError:
    ChatGoogleGenerativeAI = None
    GoogleGenerativeAIEmbeddings = None

try:
    from langchain_ollama import ChatOllama, OllamaEmbeddings
    # Or langchain_community.chat_models import ChatOllama if using older version
    # But usually langchain_ollama is preferred now. 
    # Let's assume langchain_community if langchain_ollama fails
except ImportError:
    try:
        from langchain_community.chat_models import ChatOllama
        from langchain_community.embeddings import OllamaEmbeddings
    except ImportError:
        ChatOllama = None
        OllamaEmbeddings = None
try:
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
except ImportError:
    ChatOpenAI = None
    OpenAIEmbeddings = None

class LLM:
    def __init__(self, provider: Literal["google", "ollama","openai"] = "ollama", model_name: str = None):
        self.provider = provider
        self.model_name = model_name
        
        if self.provider == "google":
            if not ChatGoogleGenerativeAI:
                raise ImportError("langchain-google-genai not installed")
            
            self.llm = ChatGoogleGenerativeAI(
                model=self.model_name or "gemini-2.5-flash",
                temperature=0,
                convert_system_message_to_human=True
            )
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
            )
            
        elif self.provider == "ollama":
            if not ChatOllama:
                raise ImportError("langchain-ollama or langchain-community not installed")

            base_url = self._get_ollama_base_url()

            # Default to llama3 for chat if not specified
            chat_model = self.model_name or "mistral"
            # User specifically requested nomic-embed-text for embeddings
            embed_model = "nomic-embed-text"

            self.llm = ChatOllama(model=chat_model, temperature=0, base_url=base_url)
            self.embeddings = OllamaEmbeddings(model=embed_model, base_url=base_url)
            
        elif self.provider == "openai":
            if not ChatOpenAI:
                raise ImportError("langchain-openai not installed")


            self.llm = ChatOpenAI(
                model=self.model_name or "gpt-4.1-nano",
                temperature=0,
            )
            self.embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
            )

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _get_ollama_base_url(self):
        base_url = os.environ.get("OLLAMA_BASE_URL")
        if not base_url:
            try:
                from django.conf import settings

                base_url = getattr(settings, "OLLAMA_BASE_URL", None)
            except ImportError:
                pass
        return base_url

    def _get_google_api_key(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            try:
                from django.conf import settings
                api_key = getattr(settings, "GOOGLE_API_KEY", None)
            except ImportError:
                pass
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        return api_key

    def invoke(self, *args, **kwargs):
        return self.llm.invoke(*args, **kwargs)


    @staticmethod
    def get_embedding_model():
        EMBEDING_MODEL = os.environ.get("EMBEDING_MODEL")
        return LLM(provider=EMBEDING_MODEL).embeddings
    
    @staticmethod
    def get_intent_analyzer_model():
        INTENT_ANALYZER_MODEL = os.environ.get("INTENT_ANALYZER_MODEL")
        return LLM(provider=INTENT_ANALYZER_MODEL.split("::")[0], model_name=INTENT_ANALYZER_MODEL.split("::")[1])
    @staticmethod
    def get_attribute_extraction_model():
        ATTRIBUTE_EXTRACTION_MODEL = os.environ.get("ATTRIBUTE_EXTRACTION_MODEL")
        return LLM(provider=ATTRIBUTE_EXTRACTION_MODEL.split("::")[0], model_name=ATTRIBUTE_EXTRACTION_MODEL.split("::")[1])

    @staticmethod
    def get_generation_model():
        GENERATION_MODEL = os.environ.get("GENERATION_MODEL")
        return LLM(provider=GENERATION_MODEL.split("::")[0], model_name=GENERATION_MODEL.split("::")[1])

# response = llm.invoke("Reply with OK")
# print(response.content)

