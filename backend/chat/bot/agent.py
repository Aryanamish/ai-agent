import logging
from typing import Any, Dict, List, Literal, Optional, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph

from chat.models import ChatMessages, ChatRoom

from .llm import LLMService

logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    query: str
    room_id: int
    intent: Optional[str]
    history: List[BaseMessage]
    response: Optional[Dict[str, Any]]
    final_response_text: Optional[str]


class ChatBot:
    def __init__(self):
        self.llm_service = LLMService()
        self.workflow = self._build_graph()
        self.app = self.workflow.compile()
        self.visualize_workflow("chatbot_workflow.png")

    def visualize_workflow(self, output_path: str):
        """Generate a visual representation of the workflow."""
        # Image(self.app.get_graph().draw_mermaid_png())
        pass

    def _build_graph(self):
        builder = StateGraph(AgentState)

        # 1. Analyze intent
        builder.add_node("analyze_intent", self.analyze_intent)
        # 2. Retrieve conversation history
        builder.add_node("retrieve_history", self.retrieve_history)
        # 3. Generate contextual response using LLM
        builder.add_node("generate_response", self.generate_response)
        # 4. Save and return response
        builder.add_node("save_conversation", self.save_conversation)

        builder.set_entry_point("analyze_intent")

        # Flow
        builder.add_edge("analyze_intent", "retrieve_history")
        builder.add_edge("retrieve_history", "generate_response")
        builder.add_edge("generate_response", "save_conversation")
        builder.add_edge("save_conversation", END)

        return builder

    def analyze_intent(self, state: AgentState) -> Dict[str, Any]:
        """Node 1: Identify the user's intent."""
        query = state["query"]
        try:
            result = self.llm_service.analyze_intent(query)
            intent = result.intent
        except Exception as e:
            logger.error(f"Intent analysis failed: {e}")
            # Fallback intent or error handling
            intent = "support_request"

        return {"intent": intent}

    def retrieve_history(self, state: AgentState) -> Dict[str, Any]:
        """Node 2: Retrieve past messages for context."""
        room_id = state["room_id"]
        # Fetch last 10 messages
        msgs = ChatMessages.objects.filter(room_id=room_id).order_by("-timestamp")[:10]

        history: List[BaseMessage] = []
        # Reverse to get chronological order
        for msg in reversed(list(msgs)):
            if msg.sender == "user":
                history.append(HumanMessage(content=msg.message))
            else:
                history.append(AIMessage(content=msg.message))

        return {"history": history}

    def generate_response(self, state: AgentState) -> Dict[str, Any]:
        """Node 3: Generate response based on intent."""
        intent = state["intent"]
        query = state["query"]
        history = state["history"]

        content = ""
        metadata = {}

        if intent == "greeting":
            system_instruction = (
                "You are a friendly customer support AI for an e-commerce platform. "
                "Greet the user warmly and ask how you can assist them today."
            )
            content = self.llm_service.generate_chat_response(
                query, history, system_instruction=system_instruction
            )
        elif intent == "product_inquiry":
            content = "Product inquiry is not implemented yet."
            metadata = {"status": "not_implemented"}
        elif intent == "support_request":
            content = "Support request is not implemented yet."
            metadata = {"status": "not_implemented"}
        else:
            content = "I'm not sure how to help with that."
            metadata = {"status": "unknown_intent"}

        response_payload = {"content": content, "intent": intent, "metadata": metadata}

        return {"response": response_payload, "final_response_text": content}

    def save_conversation(self, state: AgentState) -> Dict[str, Any]:
        """Node 4: Save the interaction to the database."""
        room_id = state["room_id"]
        query = state["query"]
        response_text = state["final_response_text"]

        if room_id:
            try:
                room = ChatRoom.objects.get(id=room_id)
                # Ensure we save the user's query and the bot's response
                # Note: If the controller already saved the user message, we might duplicate.
                # Assuming the agent is responsible for full persistence cycle here per requirements.
                ChatMessages.objects.create(room=room, message=query, sender="user")
                ChatMessages.objects.create(
                    room=room, message=response_text, sender="bot"
                )
            except ChatRoom.DoesNotExist:
                logger.error(f"ChatRoom {room_id} not found.")
            except Exception as e:
                logger.error(f"Error saving messages: {e}")

        return state

    def process_message(self, message: str, room_id: int) -> Dict[str, Any]:
        """Entry point for the bot."""
        initial_state: AgentState = {
            "query": message,
            "room_id": room_id,
            "intent": None,
            "history": [],
            "response": None,
            "final_response_text": None,
        }

        try:
            result = self.app.invoke(initial_state)
            return result.get(
                "response",
                {"content": "Internal Error", "intent": "error", "metadata": {}},
            )
        except Exception as e:
            logger.exception("Error processing message")
            return {
                "content": "Sorry, something went wrong.",
                "intent": "error",
                "metadata": {"error": str(e)},
            }
