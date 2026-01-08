import json
import logging
from typing import TypedDict, List, Dict, Any

from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from llm.llm import LLM
from organization.models import BotSettings
from organization.search import search_products

logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    input: str
    chat_history: List[Any]
    intent: str
    extracted_attributes: Dict[str, Any]
    missing_attributes: List[str]
    search_results: List[Dict[str, Any]]
    final_response: str
    org_slug: str
    bot_settings: Any # Ideally we don't pass DB object, but for simplicity

def analyze_intent(state: AgentState):
    """Classifies query into 'general' or 'product_search'."""
    prompt = state['bot_settings'].intent_prompt
    query = state['input']
    
    llm = LLM(provider="ollama", model_name="deepseek-r1")
    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=f"Query: {query}")
    ]
    
    response = llm.invoke(messages)
    content = response.content.strip().lower()
    
    if "product" in content or "search" in content or "buy" in content:
        return {"intent": "product_search"}
    return {"intent": "general"}

def general_response(state: AgentState):
    """Handles general queries."""
    system_prompt = state['bot_settings'].system_prompt
    history = state['chat_history']
    query = state['input']
    
    llm = LLM(provider="ollama", model_name="deepseek-r1")
    messages = [SystemMessage(content=system_prompt)] + history + [HumanMessage(content=query)]
    
    response = llm.invoke(messages)
    return {"final_response": response.content}

def extract_attributes(state: AgentState):
    """Extracts attributes from the query."""
    settings = state['bot_settings']
    prompt = settings.attribute_extraction_prompt
    required = settings.required_attributes
    query = state['input']
    
    # Merge history for better context? For now just query.
    llm = LLM(provider="ollama", model_name="deepseek-r1")
    messages = [
        SystemMessage(content=f"{prompt}\nRequired Attributes Scheme: {json.dumps(required)}\nReturn ONLY JSON."),
        HumanMessage(content=f"Query: {query}")
    ]
    
    response = llm.invoke(messages)
    try:
        # cleanup markdown code blocks if any
        content = response.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
            
        extracted = json.loads(content.strip())
        # Merge with existing extracted if we were looping (not implemented in this simple flow yet)
        return {"extracted_attributes": extracted}
    except Exception as e:
        logger.error(f"Failed to parse attributes: {e}")
        return {"extracted_attributes": {}}

def check_attributes(state: AgentState):
    """Checks if required attributes are present."""
    required = state['bot_settings'].required_attributes
    extracted = state.get('extracted_attributes', {})
    missing = []
    
    # Simple check: keys in required must be in extracted (and not None)
    if isinstance(required, dict):
        for key in required.keys():
            if key not in extracted or not extracted[key]:
                 missing.append(key)
    
    return {"missing_attributes": missing}

def ask_missing(state: AgentState):
    """Generates a question to ask for missing attributes."""
    settings = state['bot_settings']
    missing = state['missing_attributes']
    prompt = settings.missing_attribute_prompt
    
    llm = LLM(provider="ollama", model_name="deepseek-r1")
    messages = [
        SystemMessage(content=f"{prompt}\nMissing fields: {', '.join(missing)}\nYou are a helpful customer service agent. The user provided some info but missed these details."),
        HumanMessage(content="Ask the user for these missing details. Be direct, polite, and brief. Do not offer options. Ask a single clear question.")
    ]
    
    response = llm.invoke(messages)
    # Cleanup potential thought chains from reasoning models
    content = response.content
    if "</thought>" in content:
        content = content.split("</thought>")[-1]
    
    return {"final_response": content.strip()}

def search_node(state: AgentState):
    """Performs vector search."""
    query = state['input']
    org_slug = state['org_slug']
    # Maybe add attributes to query for better semantic match
    # Or filter post-search. For now, simple semantic search.
    
    results = search_products(query, org_slug, top_k=5)
    return {"search_results": results}

def recommend(state: AgentState):
    """Synthesizes the recommendation response."""
    settings = state['bot_settings']
    results = state['search_results']
    prompt = settings.product_recommendation_prompt
    query = state['input']
    
    context = json.dumps(results, indent=2)
    
    llm = LLM(provider="ollama", model_name="deepseek-r1")
    messages = [
        SystemMessage(content=f"{prompt}\n\nProducts Found:\n{context}"),
        HumanMessage(content=f"User Query: {query}\nProvide recommendations. Be helpful and concise.")
    ]
    
    response = llm.invoke(messages)
    content = response.content
    if "</thought>" in content:
        content = content.split("</thought>")[-1]
        
    return {"final_response": content.strip()}

def router(state: AgentState):
    """Routes based on intent and missing attributes."""
    intent = state.get('intent')
    if intent == 'general':
        return "general_response"
    
    # Product Search Path
    missing = state.get('missing_attributes')
    if missing:
        return "ask_missing"
    
    return "search_products"

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
    lambda x: "general_response" if x['intent'] == 'general' else "extract_attributes",
    {
        "general_response": "general_response",
        "extract_attributes": "extract_attributes"
    }
)

workflow.add_edge("extract_attributes", "check_attributes")

workflow.add_conditional_edges(
    "check_attributes",
    lambda x: "ask_missing" if x['missing_attributes'] else "search_products",
    {
        "ask_missing": "ask_missing",
        "search_products": "search_products"
    }
)

workflow.add_edge("search_products", "recommend")
workflow.add_edge("general_response", END)
workflow.add_edge("ask_missing", END) # In a real app we'd pause here, but for now we return the question
workflow.add_edge("recommend", END)

app = workflow.compile()

def run_agent(input_text, chat_history, org_slug, bot_settings):
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
    
    # We want to stream the output. 
    # LangGraph .stream() returns standard steps.
    # We need to capture the final_response generation.
    return app.stream(initial_state)
