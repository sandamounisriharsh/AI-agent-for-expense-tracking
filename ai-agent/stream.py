import streamlit as st
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import requests

# --- Setup ---
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
BASE_URL = "http://localhost:8000"

# --- Tool schemas ---
class AddExpenseInput(BaseModel):
    amount: float = Field(description="The expense amount in rupees")
    category: str = Field(description="Expense category, e.g. food, travel, rent")
    description: str = Field(description="Short description of the expense")

class GetTotalInput(BaseModel):
    category: str = Field(default=None, description="Category to filter by; leave empty for total across all categories")

# --- Tools ---
@tool(args_schema=AddExpenseInput)
def add_expense(amount: float, category: str, description: str) -> str:
    """Add a new expense record."""
    try:
        r = requests.post(f"{BASE_URL}/expenses", json={
            "amount": amount, "category": category, "description": description
        }, timeout=5)
        r.raise_for_status()
        return str(r.json())
    except requests.exceptions.ConnectionError:
        return "Error: couldn't connect to the expense API. Is the FastAPI server running?"
    except requests.exceptions.Timeout:
        return "Error: the expense API took too long to respond."
    except requests.exceptions.HTTPError as e:
        return f"Error: the API rejected this request ({e})."

@tool(args_schema=GetTotalInput)
def get_total_by_category(category: str = None) -> str:
    """Get the total amount spent, optionally filtered by category."""
    try:
        params = {"category": category} if category else {}
        r = requests.get(f"{BASE_URL}/expenses/total", params=params, timeout=5)
        r.raise_for_status()
        return str(r.json())
    except requests.exceptions.ConnectionError:
        return "Error: couldn't connect to the expense API. Is the FastAPI server running?"
    except requests.exceptions.Timeout:
        return "Error: the expense API took too long to respond."
    except requests.exceptions.HTTPError as e:
        return f"Error: the API rejected this request ({e})."

# --- LLM + tool binding ---
tools = [add_expense, get_total_by_category]
tool_map = {t.name: t for t in tools}

llm = ChatGroq(model="openai/gpt-oss-120b", api_key=groq_key)
llm_with_tools = llm.bind_tools(tools)

# --- Streamlit UI ---
st.set_page_config(page_title="Expense Agent", page_icon="💰")
st.title("💰 Expense Agent")
st.caption("Ask me to add expenses or check totals — I'll figure out what to do.")

# session_state persists across reruns; a plain variable would not
if "messages" not in st.session_state:
    st.session_state.messages = []

# Redraw the conversation so far (only user turns and final assistant replies)
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif isinstance(msg, AIMessage) and msg.content:
        st.chat_message("assistant").write(msg.content)

user_input = st.chat_input("e.g. Add 300 for movies")

if user_input:
    st.session_state.messages.append(HumanMessage(content=user_input))
    st.chat_message("user").write(user_input)

    with st.spinner("Thinking..."):
        response = llm_with_tools.invoke(st.session_state.messages)
        st.session_state.messages.append(response)

        # Keep executing tool calls until the LLM returns a plain text answer
        while response.tool_calls:
            for call in response.tool_calls:
                tool_fn = tool_map[call["name"]]
                result = tool_fn.invoke(call["args"])
                st.session_state.messages.append(
                    ToolMessage(content=str(result), tool_call_id=call["id"])
                )
            response = llm_with_tools.invoke(st.session_state.messages)
            st.session_state.messages.append(response)

    st.chat_message("assistant").write(response.content)