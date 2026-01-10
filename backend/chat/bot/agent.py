import json
import logging
from typing import Any, Dict, List, Literal, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from pydantic import BaseModel

from llm.llm import LLM
from organization.models import BotSettings
from organization.search import search_products

from .prompts import (
    attribute_extraction_prompt,
    general_response_prompt,
    intent_classification_prompt,
    product_recommendation_prompt,
)
from .PydanticType import AttributeExtractionResponse, IntentResponse

logger = logging.getLogger(__name__)

class MessageContent(BaseModel):
    airesponse: str
    item_suggested: List[Any]


class Message(BaseModel):
    type: Literal["answer"]
    content: MessageContent


class AgentResponse(BaseModel):
    message: Message



class AgentState(TypedDict):
    input: str
    chat_history: List[Any]
    intent: str
    extracted_attributes: Dict[str, Any]
    missing_attributes: List[str]
    search_results: List[Dict[str, Any]]
    final_response: Dict[str, Any] # Changed from str to Dict (AgentResponse dumped)
    org_slug: str
    bot_settings: Any # Ideally we don't pass DB object, but for simplicity

def analyze_intent(state: AgentState):
    """Classifies query into 'general' or 'product_search'."""
    prompt = json.loads(state['bot_settings'].intent_prompt)
    query = state['input']

    llm = LLM(provider="ollama", model_name="mistral")
   
    messages = intent_classification_prompt.format_messages(
        shop_name=state['bot_settings'].name,
        user_message=query, 
        chat_history=state['chat_history'][:-1], 
        general_shopping_query_example=prompt.get('general_shopping_query_example', 'How are you today?'),
        product_search_example1=prompt.get('product_search_example1', 'Show me some running shoes'),
        product_search_example2=prompt.get('product_search_example2', 'I want to buy a red dress')
    )
    response = llm.invoke(messages)
    data = IntentResponse.model_validate_json(response.content)
    if data.intent == "product_search":
        print("Intent Analysis Response:", "product_search")
        return {"intent": "product_search"}
    print("Intent Analysis Response:", "general")
    return {"intent": "general"}

def general_response(state: AgentState):
    """Handles general queries."""
    system_prompt = state['bot_settings'].system_prompt
    
    history = state['chat_history']
    query = state['input']

    llm = LLM(provider="ollama", model_name="mistral")
    messages = general_response_prompt.format_messages(
        bot_system_prompt=system_prompt,
        chat_history=history[:-1],
        user_message=query
    )
    
    response = llm.invoke(messages)
    return {
        "final_response": AgentResponse(
            message=Message(
                type="answer",
                content=MessageContent(
                    airesponse=response.content,
                    item_suggested=[]
                )
            )
        ).model_dump()
    }

def extract_attributes(state: AgentState):
    """Extracts attributes from the query."""
    settings = state['bot_settings']
    query = state['input']
    
    # Merge history for better context? For now just query.
    llm = LLM(provider="ollama", model_name="mistral")

    messages = attribute_extraction_prompt.format_messages(
        shop_name=settings.name,
        user_message=query,
        chat_history=state['chat_history'][:-1],
        extraction_prompt=settings.attribute_extraction_prompt
    )
    response = llm.invoke(messages)
    try:
        content = AttributeExtractionResponse.model_validate_json(response.content)
        return {"extracted_attributes": content.extracted_attributes}
    except Exception as e:
        logger.error(f"Failed to parse attributes: {e}")
        return {"extracted_attributes": {}}

def check_attributes(state: AgentState):
    """Checks if any of the attributes are present."""
    required = state['bot_settings'].required_attributes
    extracted = state.get('extracted_attributes', {})
    missing = []
    
    # Simple check: keys in required must be in extracted (and not None)
    extracted_some_attributes = False
    for key in required.keys():
        if extracted[key] is not None:
            missing.append(key)
            extracted_some_attributes = True
    if not extracted_some_attributes:
        return {"missing_attributes": missing}
    return {"missing_attributes": []}

def ask_missing(state: AgentState):
    """Generates a question to ask for missing attributes."""
    settings = state['bot_settings']
    missing = state['missing_attributes']
    prompt = settings.missing_attribute_prompt

    # llm = LLM(provider="ollama", model_name="mistral")
    # messages = [
    #     SystemMessage(content=f"{prompt}\nMissing fields: {', '.join(missing)}\nYou are a helpful customer service agent. The user provided some info but missed these details."),
    #     HumanMessage(content="Ask the user for these missing details. Be direct, polite, and brief. Do not offer options. Ask a single clear question.")
    # ]
    
    # response = llm.invoke(messages)
    # # Cleanup potential thought chains from reasoning models
    # content = response.content
    # if "</thought>" in content:
    #     content = content.split("</thought>")[-1]
    
    return {
        "final_response": AgentResponse(
            message=Message(
                type="answer",
                content=MessageContent(
                    airesponse="not Implemented",
                    item_suggested=[]
                )
            )
        ).model_dump()
    }

def search_node(state: AgentState):
    """Performs vector search."""
    query = state['input']
    org_slug = state['org_slug']
    # Maybe add attributes to query for better semantic match
    # Or filter post-search. For now, simple semantic search.
    
    results = search_products(query, org_slug, top_k=15)
    return {"search_results": results}

def recommend(state: AgentState):
    """Synthesizes the recommendation response."""
    settings = state['bot_settings']
    results = state['search_results']

    llm = LLM(provider="ollama", model_name="mistral")
    messages = product_recommendation_prompt.format_messages(
        shop_name=settings.name,
        extracted_attributes=json.dumps(state['extracted_attributes']),
        user_message=state['input'],
        available_products=json.dumps(results)
    )
    
    response = llm.invoke(messages)
    sanitized_results = [{"name": item['name'], "price": item["price"], "image": item["image"], "id": item["id"]} for item in results]

    return {
        "final_response": AgentResponse(
            message=Message(
                type="answer",
                content=MessageContent(
                    airesponse=response.content,
                    item_suggested=sanitized_results
                )
            )
        ).model_dump()
    }



# Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("analyze_intent", analyze_intent)
workflow.add_node("general_response", general_response)
workflow.add_node("extract_attributes", extract_attributes)
workflow.add_node("check_attributes", check_attributes)
workflow.add_node("ask_missing", ask_missing)
workflow.add_node("search_products", search_node)
workflow.add_node("recommend", recommend)

workflow.set_entry_point("analyze_intent")

# Edges
workflow.add_conditional_edges(
    "analyze_intent",
    lambda x: "general_response" if x["intent"] == "general" else "extract_attributes",
)

workflow.add_edge("extract_attributes", "check_attributes")

workflow.add_conditional_edges(
    "check_attributes",
    lambda x: "ask_missing" if x["missing_attributes"] else "search_products",
)

workflow.add_edge("search_products", "recommend")
workflow.add_edge("general_response", END)
workflow.add_edge("ask_missing", END) # In a real app we'd pause here, but for now we return the question
workflow.add_edge("recommend", END)

app = workflow.compile()

def run_agent(input_text, chat_history, org_slug, bot_settings, session_id: str = None):
    """Entry point to run the graph properly."""
    initial_state = {
        "input": input_text,
        "chat_history": chat_history,
        "org_slug": org_slug,
        "bot_settings": bot_settings,
        "extracted_attributes": {},
        "missing_attributes": [],
        "search_results": []
    }

    config = {}
    if session_id:
        config["metadata"] = {"session_id": session_id}
        config["run_name"] = f"{org_slug} ({session_id})"

    # We want to stream the output. 
    # LangGraph .stream() returns standard steps.
    # We need to capture the final_response generation.
    return app.stream(initial_state, config=config, stream_mode="updates")
