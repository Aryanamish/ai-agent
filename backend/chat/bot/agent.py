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
    missing_attributes_prompt
)
from .PydanticType import AttributeExtractionResponse, IntentResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# logger.basicConfig(level=logging.DEBUG)


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

import json
import re

def extract_and_sanitize_json(llm_output: str):
    """
    Takes a string input (e.g., from an LLM) and attempts to extract
    and parse the first valid JSON object or array found within it.
    
    Returns:
        dict | list | None: The parsed JSON object/list, or None if parsing fails.
    """
    if not llm_output or not isinstance(llm_output, str):
        return llm_output

    try:
        # 1. Search for the first '{' or '[' to identify start of JSON
        match = re.search(r'[\{\[]', llm_output)
        if not match:
            return llm_output
        
        start_index = match.start()
        start_char = llm_output[start_index]
        
        # 2. Determine the expected closing character
        end_char = '}' if start_char == '{' else ']'
        
        # 3. Find the last occurrence of the closing character
        # We search from the end to capture the outermost block
        end_index = llm_output.rfind(end_char)
        
        if end_index == -1 or end_index < start_index:
            return llm_output

        # 4. Extract the candidate substring
        json_candidate = llm_output[start_index : end_index + 1]

        return json_candidate

    except (json.JSONDecodeError, ValueError, Exception):
        # The function must not throw an error, so we catch everything
        # and return None (or you could return an empty dict {})
        return llm_output


def analyze_intent(state: AgentState):
    """Classifies query into 'general' or 'product_search'."""
    prompt = json.loads(state['bot_settings'].intent_prompt)
    query = state['input']

    llm = LLM.get_intent_analyzer_model()
   
    messages = intent_classification_prompt.format_messages(
        shop_name=state['bot_settings'].name,
        user_message=query, 
        chat_history=state['chat_history'], 
        general_shopping_query_example=prompt.get('general_shopping_query_example', 'How are you today?'),
        product_search_example1=prompt.get('product_search_example1', 'Show me some running shoes'),
        product_search_example2=prompt.get('product_search_example2', 'I want to buy a red dress')
    )
    response = llm.invoke(messages)
    data = IntentResponse.model_validate_json(extract_and_sanitize_json(response.content))
    if data.intent == "product_search":
        logger.info("Intent Analysis Response: product_search")
        return {"intent": "product_search"}
    logger.info("Intent Analysis Response: general")
    return {"intent": "general"}

def general_response(state: AgentState):
    """Handles general queries."""
    logger.info("generating general response")
    system_prompt = state['bot_settings'].system_prompt
    
    history = state['chat_history']
    query = state['input']

    llm = LLM.get_generation_model()
    messages = general_response_prompt.format_messages(
        bot_system_prompt=system_prompt,
        chat_history=history,
        user_message=query
    )
    
    response = llm.invoke(messages)
    logger.debug(f"General Response LLM output: {response.content}")
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
    logger.info("Extracting attributes")
    settings = state['bot_settings']
    query = state['input']
    
    # Merge history for better context? For now just query.
    llm = LLM.get_attribute_extraction_model()

    messages = attribute_extraction_prompt.format_messages(
        shop_name=settings.name,
        user_message=query,
        chat_history=state['chat_history'],
        extracted_attributes=json.dumps(state['extracted_attributes']),
        extraction_prompt=settings.attribute_extraction_prompt
    )
    response = llm.invoke(messages)
    logger.debug(f"extract_attributes Response LLM output: {response.content}")
    try:
        content = AttributeExtractionResponse.model_validate_json(extract_and_sanitize_json(response.content))
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
        if extracted.get(key, None) is None:
            missing.append(key)
        else:
            extracted_some_attributes = True
    if not extracted_some_attributes:
        logger.info("No attributes extracted")
        return {"missing_attributes": missing}
    logger.info("Got some attributes continuing")
    return {"missing_attributes": []}

def ask_missing(state: AgentState):
    """Generates a question to ask for missing attributes."""
    logger.info("Asking for missing attributes")
    settings = state['bot_settings']
    missing = state['missing_attributes']

    messages = missing_attributes_prompt.format_messages(
        shop_name=settings.name,
        missing_attributes=", ".join(missing),
        extracted_attributes=json.dumps(state['extracted_attributes']),
        chat_history=state['chat_history'],
        user_message=state['input'],
        missing=", ".join(missing),
    )
    llm = LLM.get_generation_model()
    
    response = llm.invoke(messages)

    try:
        logger.debug(f"Missing Attributes LLM output: {response.content}")
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
    except Exception as e:
        logger.error(f"Failed to parse missing attribute question: {e}")
        return {
            "final_response": AgentResponse(
                message=Message(
                    type="answer",
                    content=MessageContent(
                        airesponse="Could you please provide more details about what you're looking for?",
                        item_suggested=[]
                    )
                )
            ).model_dump()
        }
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
    logger.info("Performing product search")
    query = state['input']
    ext_attr = state["extracted_attributes"]
    query += " ".join([f"{k}: {v}" for k, v in ext_attr.items()])
    org_slug = state['org_slug']
    # Maybe add attributes to query for better semantic match
    # Or filter post-search. For now, simple semantic search.
    
    results = search_products(query, org_slug, top_k=15)
    return {"search_results": results}

def recommend(state: AgentState):
    """Synthesizes the recommendation response."""
    logger.info("Generating product recommendations")
    settings = state['bot_settings']
    results = state['search_results']

    llm = LLM.get_generation_model()
    messages = product_recommendation_prompt.format_messages(
        shop_name=settings.name,
        extracted_attributes=json.dumps(state['extracted_attributes']),
        user_message=state['input'],
        available_products=json.dumps([{"name": r["name"], "price": r["price"]} for r in results])
    )
    
    response = llm.invoke(messages)
    sanitized_results = [{"name": item['name'], "price": item["price"], "image": item["image"]} for item in results]
    logger.debug(f"Product Recommendation LLM output: {response.content}")
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

def run_agent(input_text, chat_history, org_slug, bot_settings, room):
    """Entry point to run the graph properly."""
    initial_state = {
        "input": input_text,
        "chat_history": chat_history,
        "org_slug": org_slug,
        "bot_settings": bot_settings,
        "extracted_attributes": room.extracted_attributes or {},
        "missing_attributes": room.missing_attributes or [],
        "search_results": []
    }
    logger.info(f"Running agent for org: {org_slug} with input: {input_text}")
    config = {}
    if room.pk:
        config["metadata"] = {"session_id": room.pk}
        config["run_name"] = f"{org_slug} ({room.pk})"

    # We want to stream the output. 
    # LangGraph .stream() returns standard steps.
    # We need to capture the final_response generation.
    return app.stream(initial_state, config=config, stream_mode="updates")
