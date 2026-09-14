import os
import json
import requests
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

BASE_URL = os.getenv(
    "BASE_URL",
    "http://localhost:8000"
)

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set in .env"
    )


# ============================================================
# SYSTEM PROMPT
# ============================================================

PROMPT_PATH = (
    Path(__file__).parent
    / "prompts"
    / "system_prompt.txt"
)

if not PROMPT_PATH.exists():
    raise FileNotFoundError(
        f"System prompt not found: {PROMPT_PATH}"
    )

SYSTEM_PROMPT = PROMPT_PATH.read_text(
    encoding="utf-8"
)


# ============================================================
# INPUT SCHEMAS
# ============================================================

class AddExpenseInput(BaseModel):
    amount: float = Field(
        description="Amount of the new expense"
    )

    category: str = Field(
        description="Category of the new expense"
    )

    description: str = Field(
        description="Description of the new expense"
    )


class ExpenseItem(BaseModel):
    amount: float
    category: str
    description: str = ""


class AddExpensesInput(BaseModel):
    expenses: list[ExpenseItem]


class GetTotalInput(BaseModel):
    category: str | None = Field(
        default=None,
        description="Optional category to calculate the total for"
    )


class GetExpensesInput(BaseModel):
    category: str | None = Field(
        default=None,
        description="Optional category to filter expenses"
    )


class AnalyzeExpensesInput(BaseModel):
    category: str | None = Field(
        default=None,
        description="Optional category to analyze"
    )


class FindExpenseInput(BaseModel):
    description: str | None = Field(
        default=None,
        description=(
            "Words or description identifying "
            "the existing expense"
        )
    )

    category: str | None = Field(
        default=None,
        description=(
            "Category identifying the existing expense"
        )
    )

    amount: float | None = Field(
        default=None,
        description=(
            "Existing amount of the expense, "
            "if the user specifies it"
        )
    )

    new_amount: float | None = Field(
        default=None,
        description=(
            "New amount requested by the user "
            "when editing"
        )
    )

    new_category: str | None = Field(
        default=None,
        description=(
            "New category requested by the user "
            "when editing"
        )
    )

    new_description: str | None = Field(
        default=None,
        description=(
            "New description requested by the user "
            "when editing"
        )
    )


class DeleteExpenseInput(BaseModel):
    expense_id: int = Field(
        description="Internal expense ID"
    )


class EditExpenseInput(BaseModel):
    expense_id: int = Field(
        description="Internal expense ID"
    )

    amount: float | None = Field(
        default=None,
        description="New amount"
    )

    category: str | None = Field(
        default=None,
        description="New category"
    )

    description: str | None = Field(
        default=None,
        description="New description"
    )


# ============================================================
# CREATE TOOLS
# ============================================================

def create_tools(access_token: str):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # ========================================================
    # ADD EXPENSE
    # ========================================================

    @tool(args_schema=AddExpenseInput)
    def add_expense(
        amount: float,
        category: str,
        description: str,
    ) -> str:
        """
        Add a new expense for the authenticated user.
        """

        try:
            response = requests.post(
                f"{BASE_URL}/expenses",
                headers={
                    **headers,
                    "Content-Type": "application/json",
                },
                json={
                    "amount": amount,
                    "category": category,
                    "description": description,
                },
                timeout=10,
            )

            if not response.ok:
                return json.dumps({
                    "success": False,
                    "message": response.text,
                })

            return json.dumps({
                "success": True,
                "message": "Expense added successfully",
                "expense": response.json(),
            })

        except requests.RequestException as e:
            return json.dumps({
                "success": False,
                "message": str(e),
            })

    # ========================================================
    # ADD MULTIPLE EXPENSES
    # ========================================================

    @tool(args_schema=AddExpensesInput)
    def add_expenses(
        expenses: list[ExpenseItem],
    ) -> str:
        """
        Add multiple expenses for the authenticated user.
        """

        results = []

        try:
            for expense in expenses:

                response = requests.post(
                    f"{BASE_URL}/expenses",
                    headers={
                        **headers,
                        "Content-Type": "application/json",
                    },
                    json={
                        "amount": expense.amount,
                        "category": expense.category,
                        "description": expense.description,
                    },
                    timeout=10,
                )

                if not response.ok:

                    results.append({
                        "success": False,
                        "message": response.text,
                        "expense": {
                            "amount": expense.amount,
                            "category": expense.category,
                            "description": expense.description,
                        },
                    })

                else:

                    results.append({
                        "success": True,
                        "expense": response.json(),
                    })

            successful = sum(
                1
                for result in results
                if result["success"]
            )

            return json.dumps({
                "success": (
                    successful == len(expenses)
                ),
                "message": (
                    f"{successful} of "
                    f"{len(expenses)} expenses "
                    "added successfully"
                ),
                "results": results,
            })

        except requests.RequestException as e:

            return json.dumps({
                "success": False,
                "message": str(e),
            })

    # ========================================================
    # GET TOTAL
    # ========================================================

    @tool(args_schema=GetTotalInput)
    def get_total(
        category: str | None = None,
    ) -> str:
        """
        Get the user's total spending.
        """

        try:

            params = {}

            if category:
                params["category"] = category

            response = requests.get(
                f"{BASE_URL}/expenses/total",
                headers=headers,
                params=params,
                timeout=10,
            )

            if not response.ok:

                return json.dumps({
                    "success": False,
                    "message": response.text,
                })

            data = response.json()

            return json.dumps({
                "success": True,
                "category": category or "all",
                "total": data.get(
                    "total",
                    0
                ),
            })

        except requests.RequestException as e:

            return json.dumps({
                "success": False,
                "message": str(e),
            })

    # ========================================================
    # GET EXPENSES
    # ========================================================

    @tool(args_schema=GetExpensesInput)
    def get_expenses(
        category: str | None = None,
    ) -> str:
        """
        Get the user's expenses.
        """

        try:

            params = {}

            if category:
                params["category"] = category

            response = requests.get(
                f"{BASE_URL}/expenses",
                headers=headers,
                params=params,
                timeout=10,
            )

            if not response.ok:

                return json.dumps({
                    "success": False,
                    "message": response.text,
                })

            expenses = response.json()

            total = sum(
                float(expense["amount"])
                for expense in expenses
            )

            category_totals = {}

            for expense in expenses:

                category_name = expense[
                    "category"
                ]

                category_totals[category_name] = (
                    category_totals.get(
                        category_name,
                        0
                    )
                    + float(expense["amount"])
                )

            return json.dumps({
                "success": True,
                "expenses": expenses,
                "count": len(expenses),
                "total": total,
                "category_totals": category_totals,
            })

        except requests.RequestException as e:

            return json.dumps({
                "success": False,
                "message": str(e),
            })

    # ========================================================
    # ANALYZE EXPENSES
    # ========================================================

    @tool(args_schema=AnalyzeExpensesInput)
    def analyze_expenses(
        category: str | None = None,
    ) -> str:
        """
        Analyze the user's spending.
        """

        try:

            params = {}

            if category:
                params["category"] = category

            response = requests.get(
                f"{BASE_URL}/expenses",
                headers=headers,
                params=params,
                timeout=10,
            )

            if not response.ok:

                return json.dumps({
                    "success": False,
                    "message": response.text,
                })

            expenses = response.json()

            if not expenses:

                return json.dumps({
                    "success": True,
                    "count": 0,
                    "total": 0,
                    "average": 0,
                    "category_totals": {},
                    "category_percentages": {},
                    "largest_category": None,
                    "largest_expense": None,
                })

            amounts = [
                float(expense["amount"])
                for expense in expenses
            ]

            total = sum(amounts)

            average = (
                total / len(amounts)
            )

            category_totals = {}

            for expense in expenses:

                category_name = expense[
                    "category"
                ]

                category_totals[category_name] = (
                    category_totals.get(
                        category_name,
                        0
                    )
                    + float(expense["amount"])
                )

            category_percentages = {}

            for (
                category_name,
                category_total
            ) in category_totals.items():

                percentage = (
                    category_total / total * 100
                    if total > 0
                    else 0
                )

                category_percentages[
                    category_name
                ] = round(
                    percentage,
                    2
                )

            largest_category = max(
                category_totals,
                key=category_totals.get
            )

            largest_expense = max(
                expenses,
                key=lambda expense:
                float(expense["amount"])
            )

            return json.dumps({
                "success": True,
                "count": len(expenses),
                "total": round(
                    total,
                    2
                ),
                "average": round(
                    average,
                    2
                ),
                "category_totals":
                    category_totals,
                "category_percentages":
                    category_percentages,
                "largest_category":
                    largest_category,
                "largest_expense":
                    largest_expense,
            })

        except requests.RequestException as e:

            return json.dumps({
                "success": False,
                "message": str(e),
            })

    # ========================================================
    # FIND EXPENSES
    # ========================================================

    @tool(args_schema=FindExpenseInput)
    def find_expenses(
        description: str | None = None,
        category: str | None = None,
        amount: float | None = None,
        new_amount: float | None = None,
        new_category: str | None = None,
        new_description: str | None = None,
    ) -> str:
        """
        Find existing expenses using natural language.

        Internal IDs are returned to the agent but must
        never be shown to the user.

        new_amount, new_category and new_description
        are used only to preserve requested edit values.
        """

        def normalize_word(word: str):

            word = (
                word.lower()
                .strip()
            )

            # groceries -> grocery
            if (
                word.endswith("ies")
                and len(word) > 4
            ):
                word = (
                    word[:-3]
                    + "y"
                )

            # expenses -> expense
            elif (
                word.endswith("s")
                and len(word) > 3
            ):
                word = word[:-1]

            return word

        def normalize_text(text: str):

            cleaned = (
                text.lower()
                .replace(",", " ")
                .replace(".", " ")
                .replace("₹", " ")
            )

            words = cleaned.split()

            return [
                normalize_word(word)
                for word in words
                if len(word) > 2
            ]

        try:

            response = requests.get(
                f"{BASE_URL}/expenses",
                headers=headers,
                timeout=10,
            )

            if not response.ok:

                return json.dumps({
                    "success": False,
                    "message": response.text,
                })

            expenses = response.json()

            ignored_words = {
                "expense",
                "expenses",
                "purchase",
                "purchases",
                "item",
                "items",
                "payment",
                "payments",
                "the",
                "my",
                "this",
                "that",
                "please",
                "delete",
                "remove",
                "edit",
                "change",
                "update",
            }

            description_words = []

            if description:

                description_words = [
                    word
                    for word in normalize_text(
                        description
                    )
                    if word not in ignored_words
                ]

            category_words = []

            if category:

                category_words = [
                    word
                    for word in normalize_text(
                        category
                    )
                    if word not in ignored_words
                ]

            matches = []

            for expense in expenses:

                expense_description_words = set(
                    normalize_text(
                        str(
                            expense["description"]
                        )
                    )
                )

                expense_category_words = set(
                    normalize_text(
                        str(
                            expense["category"]
                        )
                    )
                )

                # ----------------------------------------
                # DESCRIPTION
                # ----------------------------------------

                description_match = True

                if description_words:

                    description_match = any(
                        (
                            query_word
                            in expense_description_words
                        )
                        or any(
                            (
                                query_word
                                in expense_word
                            )
                            or (
                                expense_word
                                in query_word
                            )
                            for expense_word
                            in expense_description_words
                        )
                        for query_word
                        in description_words
                    )

                # ----------------------------------------
                # CATEGORY
                # ----------------------------------------

                category_match = True

                if category_words:

                    category_match = any(
                        (
                            query_word
                            in expense_category_words
                        )
                        or any(
                            (
                                query_word
                                in expense_word
                            )
                            or (
                                expense_word
                                in query_word
                            )
                            for expense_word
                            in expense_category_words
                        )
                        for query_word
                        in category_words
                    )

                # ----------------------------------------
                # EXISTING AMOUNT
                # ----------------------------------------

                amount_match = True

                if amount is not None:

                    amount_match = (
                        abs(
                            float(
                                expense["amount"]
                            )
                            - float(amount)
                        )
                        < 0.01
                    )

                # ----------------------------------------
                # FINAL MATCH
                # ----------------------------------------

                if (
                    description_match
                    and category_match
                    and amount_match
                ):

                    matches.append(
                        expense
                    )

            return json.dumps({
                "success": True,
                "matches": matches,
                "count": len(matches),

                # Preserve requested edit values
                "requested_changes": {
                    "amount": new_amount,
                    "category": new_category,
                    "description":
                        new_description,
                },
            })

        except requests.RequestException as e:

            return json.dumps({
                "success": False,
                "message": str(e),
            })

    # ========================================================
    # DELETE EXPENSE
    # ========================================================

    @tool(args_schema=DeleteExpenseInput)
    def delete_expense(
        expense_id: int,
    ) -> str:
        """
        Permanently delete an expense.

        This function is only called internally after
        explicit user confirmation.
        """

        try:

            response = requests.delete(
                f"{BASE_URL}/expenses/{expense_id}",
                headers=headers,
                timeout=10,
            )

            if response.status_code == 404:

                return json.dumps({
                    "success": False,
                    "message": "Expense not found",
                })

            if not response.ok:

                return json.dumps({
                    "success": False,
                    "message": response.text,
                })

            return json.dumps({
                "success": True,
                "message":
                    "Expense deleted successfully",
            })

        except requests.RequestException as e:

            return json.dumps({
                "success": False,
                "message": str(e),
            })

    # ========================================================
    # EDIT EXPENSE
    # ========================================================

    @tool(args_schema=EditExpenseInput)
    def edit_expense(
        expense_id: int,
        amount: float | None = None,
        category: str | None = None,
        description: str | None = None,
    ) -> str:
        """
        Update an expense.

        This function is only called internally after
        explicit user confirmation.
        """

        try:

            payload = {}

            if amount is not None:
                payload["amount"] = amount

            if category is not None:
                payload["category"] = category

            if description is not None:
                payload["description"] = description

            response = requests.patch(
                f"{BASE_URL}/expenses/{expense_id}",
                headers={
                    **headers,
                    "Content-Type":
                        "application/json",
                },
                json=payload,
                timeout=10,
            )

            if response.status_code == 404:

                return json.dumps({
                    "success": False,
                    "message": "Expense not found",
                })

            if not response.ok:

                return json.dumps({
                    "success": False,
                    "message": response.text,
                })

            return json.dumps({
                "success": True,
                "message":
                    "Expense updated successfully",
                "expense":
                    response.json(),
            })

        except requests.RequestException as e:

            return json.dumps({
                "success": False,
                "message": str(e),
            })

    # ========================================================
    # RETURN ALL TOOLS
    # ========================================================

    return [
        add_expense,
        add_expenses,
        get_total,
        get_expenses,
        analyze_expenses,
        find_expenses,
        delete_expense,
        edit_expense,
    ]


# ============================================================
# LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=GROQ_API_KEY,
    temperature=0.2,
)


# ============================================================
# HELPERS
# ============================================================

def extract_tool_calls(message):

    return (
        getattr(
            message,
            "tool_calls",
            []
        )
        or []
    )


def format_expense(expense):

    return (
        f"₹{float(expense['amount']):.2f} "
        f"{expense['category']} expense "
        f"for {expense['description']}"
    )


def is_yes(text: str):

    return text.strip().lower() in {
        "yes",
        "y",
        "yeah",
        "yep",
        "sure",
        "confirm",
        "confirmed",
        "do it",
        "go ahead",
        "delete it",
        "update it",
    }


def is_no(text: str):

    return text.strip().lower() in {
        "no",
        "n",
        "nope",
        "cancel",
        "don't",
        "dont",
        "stop",
    }


def get_selection_index(text: str):

    value = (
        text.strip()
        .lower()
    )

    selections = {
        "first": 0,
        "first one": 0,
        "1": 0,
        "one": 0,

        "second": 1,
        "second one": 1,
        "2": 1,
        "two": 1,

        "third": 2,
        "third one": 2,
        "3": 2,
        "three": 2,

        "fourth": 3,
        "fourth one": 3,
        "4": 3,
        "four": 3,
    }

    return selections.get(
        value
    )


# ============================================================
# RUN AGENT
# ============================================================

def run_agent(
    user_input: str,
    access_token: str,
    conversation: list | None = None,
    pending_delete: dict | None = None,
    pending_edit: dict | None = None,
    pending_selection: dict | None = None,
):

    if conversation is None:
        conversation = []

    # --------------------------------------------------------
    # CREATE TOOLS
    # --------------------------------------------------------

    tools = create_tools(
        access_token
    )

    tool_map = {
        current_tool.name:
            current_tool
        for current_tool in tools
    }

    # Only these tools are exposed to the LLM.
    #
    # delete_expense and edit_expense are deliberately
    # NOT exposed to the LLM. They are called internally
    # only after confirmation.

    agent_tools = [
        tool_map["add_expense"],
        tool_map["add_expenses"],
        tool_map["get_total"],
        tool_map["get_expenses"],
        tool_map["analyze_expenses"],
        tool_map["find_expenses"],
    ]

    # ========================================================
    # DELETE CONFIRMATION
    # ========================================================

    if pending_delete:

        if is_yes(user_input):

            result = tool_map[
                "delete_expense"
            ].invoke({
                "expense_id":
                    pending_delete[
                        "expense_id"
                    ]
            })

            try:

                parsed = json.loads(
                    result
                )

            except Exception:

                parsed = {}

            if parsed.get("success"):

                response_text = (
                    "Done — I deleted that expense."
                )

            else:

                response_text = (
                    "I couldn't delete that expense."
                )

            conversation.append(
                HumanMessage(
                    content=user_input
                )
            )

            conversation.append(
                AIMessage(
                    content=response_text
                )
            )

            return {
                "response": response_text,
                "pending_delete": None,
                "pending_edit": None,
                "pending_selection": None,
            }

        if is_no(user_input):

            response_text = (
                "Okay, I didn't delete it."
            )

            conversation.append(
                HumanMessage(
                    content=user_input
                )
            )

            conversation.append(
                AIMessage(
                    content=response_text
                )
            )

            return {
                "response": response_text,
                "pending_delete": None,
                "pending_edit": None,
                "pending_selection": None,
            }

        return {
            "response": (
                "Please confirm whether you "
                "want me to delete that expense. "
                "You can say yes or no."
            ),
            "pending_delete":
                pending_delete,
            "pending_edit": None,
            "pending_selection": None,
        }

    # ========================================================
    # EDIT CONFIRMATION
    # ========================================================

    if pending_edit:

        if is_yes(user_input):

            result = tool_map[
                "edit_expense"
            ].invoke({
                "expense_id":
                    pending_edit[
                        "expense_id"
                    ],

                "amount":
                    pending_edit.get(
                        "amount"
                    ),

                "category":
                    pending_edit.get(
                        "category"
                    ),

                "description":
                    pending_edit.get(
                        "description"
                    ),
            })

            try:

                parsed = json.loads(
                    result
                )

            except Exception:

                parsed = {}

            if parsed.get("success"):

                response_text = (
                    "Done — I updated that expense."
                )

            else:

                response_text = (
                    "I couldn't update that expense."
                )

            conversation.append(
                HumanMessage(
                    content=user_input
                )
            )

            conversation.append(
                AIMessage(
                    content=response_text
                )
            )

            return {
                "response": response_text,
                "pending_delete": None,
                "pending_edit": None,
                "pending_selection": None,
            }

        if is_no(user_input):

            response_text = (
                "Okay, I didn't change it."
            )

            conversation.append(
                HumanMessage(
                    content=user_input
                )
            )

            conversation.append(
                AIMessage(
                    content=response_text
                )
            )

            return {
                "response": response_text,
                "pending_delete": None,
                "pending_edit": None,
                "pending_selection": None,
            }

        return {
            "response": (
                "Please confirm whether you "
                "want me to update that expense. "
                "You can say yes or no."
            ),
            "pending_delete": None,
            "pending_edit":
                pending_edit,
            "pending_selection": None,
        }

    # ========================================================
    # EXPENSE SELECTION
    # ========================================================

    if pending_selection:

        selected_index = get_selection_index(
            user_input
        )

        if selected_index is None:

            return {
                "response": (
                    "Please tell me which one "
                    "you mean, such as the first "
                    "one or second one."
                ),
                "pending_delete": None,
                "pending_edit": None,
                "pending_selection":
                    pending_selection,
            }

        candidates = (
            pending_selection[
                "candidates"
            ]
        )

        if selected_index >= len(
            candidates
        ):

            return {
                "response": (
                    "That option isn't available. "
                    "Please choose one of the "
                    "expenses I listed."
                ),
                "pending_delete": None,
                "pending_edit": None,
                "pending_selection":
                    pending_selection,
            }

        selected = candidates[
            selected_index
        ]

        action = pending_selection[
            "action"
        ]

        # ----------------------------------------------------
        # DELETE SELECTED EXPENSE
        # ----------------------------------------------------

        if action == "delete":

            response_text = (
                f"Do you want me to delete "
                f"your {format_expense(selected)}?"
            )

            new_pending_delete = {
                "expense_id":
                    selected["id"],
                "expense":
                    selected,
            }

            conversation.append(
                HumanMessage(
                    content=user_input
                )
            )

            conversation.append(
                AIMessage(
                    content=response_text
                )
            )

            return {
                "response": response_text,
                "pending_delete":
                    new_pending_delete,
                "pending_edit": None,
                "pending_selection": None,
            }

        # ----------------------------------------------------
        # EDIT SELECTED EXPENSE
        # ----------------------------------------------------

        if action == "edit":

            changes = (
                pending_selection.get(
                    "changes",
                    {}
                )
            )

            change_parts = []

            if changes.get(
                "amount"
            ) is not None:

                change_parts.append(
                    "amount to "
                    f"₹{float(changes['amount']):.2f}"
                )

            if changes.get(
                "category"
            ) is not None:

                change_parts.append(
                    "category to "
                    f"{changes['category']}"
                )

            if changes.get(
                "description"
            ) is not None:

                change_parts.append(
                    "description to "
                    f"{changes['description']}"
                )

            response_text = (
                f"Do you want me to update "
                f"your {format_expense(selected)}"
            )

            if change_parts:

                response_text += (
                    " — changing the "
                    + ", ".join(
                        change_parts
                    )
                    + "?"
                )

            else:

                response_text += "?"

            new_pending_edit = {
                "expense_id":
                    selected["id"],

                "expense":
                    selected,

                "amount":
                    changes.get(
                        "amount"
                    ),

                "category":
                    changes.get(
                        "category"
                    ),

                "description":
                    changes.get(
                        "description"
                    ),
            }

            conversation.append(
                HumanMessage(
                    content=user_input
                )
            )

            conversation.append(
                AIMessage(
                    content=response_text
                )
            )

            return {
                "response": response_text,
                "pending_delete": None,
                "pending_edit":
                    new_pending_edit,
                "pending_selection": None,
            }

    # ========================================================
    # BUILD LLM MESSAGES
    # ========================================================

    messages = [
        SystemMessage(
            content=SYSTEM_PROMPT
        )
    ]

    messages.extend(
        conversation
    )

    messages.append(
        HumanMessage(
            content=user_input
        )
    )

    # ========================================================
    # FIRST LLM CALL
    # ========================================================

    model_with_tools = llm.bind_tools(
        agent_tools
    )

    response = model_with_tools.invoke(
        messages
    )

    # ========================================================
    # NO TOOL CALL
    # ========================================================

    if not extract_tool_calls(
        response
    ):

        conversation.append(
            HumanMessage(
                content=user_input
            )
        )

        conversation.append(
            AIMessage(
                content=response.content
            )
        )

        return {
            "response":
                response.content,
            "pending_delete": None,
            "pending_edit": None,
            "pending_selection": None,
        }

    # ========================================================
    # PROCESS TOOL CALLS
    # ========================================================

    for tool_call in extract_tool_calls(
        response
    ):

        tool_name = tool_call[
            "name"
        ]

        tool_args = (
            tool_call.get(
                "args",
                {}
            )
            or {}
        )

        selected_tool = tool_map.get(
            tool_name
        )

        if not selected_tool:
            continue

        # ====================================================
        # FIND EXPENSES
        # ====================================================

        if tool_name == "find_expenses":

            result = selected_tool.invoke(
                tool_args
            )

            try:

                parsed = json.loads(
                    result
                )

            except Exception:

                parsed = {}

            if not parsed.get(
                "success"
            ):

                return {
                    "response": (
                        "I couldn't retrieve "
                        "your expenses right now."
                    ),
                    "pending_delete": None,
                    "pending_edit": None,
                    "pending_selection": None,
                }

            matches = parsed.get(
                "matches",
                []
            )

            if not matches:

                return {
                    "response": (
                        "I couldn't find an "
                        "expense matching that."
                    ),
                    "pending_delete": None,
                    "pending_edit": None,
                    "pending_selection": None,
                }

            # ------------------------------------------------
            # DETERMINE ACTION
            # ------------------------------------------------

            lower_input = (
                user_input.lower()
            )

            if (
                "delete" in lower_input
                or "remove" in lower_input
            ):

                action = "delete"

            elif (
                "edit" in lower_input
                or "change" in lower_input
                or "update" in lower_input
            ):

                action = "edit"

            else:

                action = "delete"

            # ------------------------------------------------
            # GET REQUESTED EDIT VALUES
            # ------------------------------------------------

            requested_changes = (
                parsed.get(
                    "requested_changes",
                    {}
                )
            )

            new_amount = (
                requested_changes.get(
                    "amount"
                )
            )

            new_category = (
                requested_changes.get(
                    "category"
                )
            )

            new_description = (
                requested_changes.get(
                    "description"
                )
            )

            # ------------------------------------------------
            # ONE MATCH
            # ------------------------------------------------

            if len(matches) == 1:

                expense = matches[0]

                if action == "delete":

                    response_text = (
                        f"Do you want me to "
                        f"delete your "
                        f"{format_expense(expense)}?"
                    )

                    conversation.append(
                        HumanMessage(
                            content=user_input
                        )
                    )

                    conversation.append(
                        AIMessage(
                            content=response_text
                        )
                    )

                    return {
                        "response":
                            response_text,

                        "pending_delete": {
                            "expense_id":
                                expense["id"],
                            "expense":
                                expense,
                        },

                        "pending_edit":
                            None,

                        "pending_selection":
                            None,
                    }

                # --------------------------------------------
                # EDIT
                # --------------------------------------------

                change_parts = []

                if new_amount is not None:

                    change_parts.append(
                        "amount to "
                        f"₹{float(new_amount):.2f}"
                    )

                if new_category is not None:

                    change_parts.append(
                        "category to "
                        f"{new_category}"
                    )

                if new_description is not None:

                    change_parts.append(
                        "description to "
                        f"{new_description}"
                    )

                response_text = (
                    f"Do you want me to update "
                    f"your {format_expense(expense)}"
                )

                if change_parts:

                    response_text += (
                        " — changing the "
                        + ", ".join(
                            change_parts
                        )
                        + "?"
                    )

                else:

                    response_text += "?"

                conversation.append(
                    HumanMessage(
                        content=user_input
                    )
                )

                conversation.append(
                    AIMessage(
                        content=response_text
                    )
                )

                return {
                    "response":
                        response_text,

                    "pending_delete":
                        None,

                    "pending_edit": {
                        "expense_id":
                            expense["id"],

                        "expense":
                            expense,

                        "amount":
                            new_amount,

                        "category":
                            new_category,

                        "description":
                            new_description,
                    },

                    "pending_selection":
                        None,
                }

            # ------------------------------------------------
            # MULTIPLE MATCHES
            # ------------------------------------------------

            response_text = (
                f"I found {len(matches)} "
                "matching expenses:"
            )

            for index, expense in enumerate(
                matches[:4],
                start=1
            ):

                response_text += (
                    f"\n{index}. "
                    f"{format_expense(expense)}"
                )

            response_text += (
                "\nWhich one would you like "
                "to "
                + (
                    "delete?"
                    if action == "delete"
                    else "edit?"
                )
            )

            conversation.append(
                HumanMessage(
                    content=user_input
                )
            )

            conversation.append(
                AIMessage(
                    content=response_text
                )
            )

            return {
                "response":
                    response_text,

                "pending_delete":
                    None,

                "pending_edit":
                    None,

                "pending_selection": {
                    "action":
                        action,

                    "candidates":
                        matches[:4],

                    "changes": {
                        "amount":
                            new_amount,

                        "category":
                            new_category,

                        "description":
                            new_description,
                    },
                },
            }

        # ====================================================
        # NORMAL TOOLS
        # ====================================================

        result = selected_tool.invoke(
            tool_args
        )

        try:

            parsed_result = json.loads(
                result
            )

        except Exception:

            parsed_result = result

        # ----------------------------------------------------
        # NATURAL RESPONSE
        # ----------------------------------------------------

        final_prompt = f"""
Respond naturally to the user's latest request.

User:
{user_input}

Data returned by the expense system:
{json.dumps(
    parsed_result,
    ensure_ascii=False
)}

Follow the main system instructions.

Important:
- Answer directly.
- Be conversational.
- Keep it concise.
- Do not mention tools.
- Do not mention internal IDs.
- Do not expose JSON.
- Do not invent information.
- Do not add unnecessary headings.
- Do not add a generic "let me know if..." ending.
- If the user asks for expenses, give useful expense details.
- If the user asks for a simple value, give the simple value.
"""

        final_response = llm.invoke([
            SystemMessage(
                content=SYSTEM_PROMPT
            ),
            HumanMessage(
                content=final_prompt
            ),
        ])

        conversation.append(
            HumanMessage(
                content=user_input
            )
        )

        conversation.append(
            AIMessage(
                content=final_response.content
            )
        )

        return {
            "response":
                final_response.content,

            "pending_delete":
                None,

            "pending_edit":
                None,

            "pending_selection":
                None,
        }

    # ========================================================
    # FALLBACK
    # ========================================================

    return {
        "response": (
            "I'm sorry, I couldn't "
            "process that request."
        ),
        "pending_delete": None,
        "pending_edit": None,
        "pending_selection": None,
    }