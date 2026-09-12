from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.tools import tool
import requests
from langchain_core.messages import HumanMessage, ToolMessage



load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
BASE_URL = "http://localhost:8000"

class AddExpenseInput(BaseModel):
    amount: float = Field(description="The expense amount in rupees")
    category: str = Field(description="Expense category, e.g. food, travel, rent")
    description: str = Field(description="Short description of the expense")

class GetTotalInput(BaseModel):
    category:str = Field(default=None,description="Category to filter by; leave empty for total across all categories")

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

messages = []

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

llm = ChatGroq(model="openai/gpt-oss-120b", api_key=groq_key)
llm_with_tools = llm.bind_tools([add_expense])
tools = [add_expense, get_total_by_category]
tool_map = {t.name: t for t in tools}

def run_agent(user_input:str)-> str:

    messages.append(HumanMessage(content=user_input))
    response = llm_with_tools.invoke(messages)
    messages.append(response)

    while response.tool_calls:
        for call in response.tool_calls:
            tool_fn = tool_map[call["name"]]
            result = tool_fn.invoke(call["args"])
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
        response = llm_with_tools.invoke(messages)
        messages.append(response)

    return response.content

if __name__ == "__main__":
    print("Expense agent ready. Type 'quit' to exit.\n")
    try:
        while True:
            user_input = input("you: ")
            if user_input.strip().lower() in ("quit", "exit"):
                print("Goodbye!")
                break
            reply = run_agent(user_input)
            print(f"Agent: {reply}\n")

    except KeyboardInterrupt:
        print("\nGoodbye!..")
