from google.adk.agents import Agent
from google.adk.tools import ToolContext


def save_user_information(
    tool_context: ToolContext,
    user_name: str | None = None,
    learning_topic: str | None = None,
    favorite_language: str | None = None,
) -> dict:
    """Save user information into the current session state."""

    updates = {}

    if user_name:
        tool_context.state["user_name"] = user_name
        updates["user_name"] = user_name

    if learning_topic:
        tool_context.state["learning_topic"] = learning_topic
        updates["learning_topic"] = learning_topic

    if favorite_language:
        tool_context.state["favorite_language"] = favorite_language
        updates["favorite_language"] = favorite_language

    if not updates:
        return {
            "status": "error",
            "message": "No information was provided."
        }

    return {
        "status": "success",
        "updated": updates
    }


root_agent = Agent(
    name="personal_assistant",
    model="gemini-2.5-flash",

    description="A personal assistant demonstrating ADK sessions and state.",

    instruction="""
You are a helpful personal assistant.

You have access to session state.

Current state variables:

- user_name
- learning_topic
- favorite_language

When the user gives you personal information that should be
remembered, use the save_user_information tool.

Examples:

User: My name is Harsh
→ call save_user_information(user_name="Harsh")

User: I am learning Agentic AI
→ call save_user_information(learning_topic="Agentic AI")

User: My favorite programming language is Python
→ call save_user_information(favorite_language="Python")

When the user asks what you remember, answer using the current
session state.

Keep responses concise.
""",

    tools=[save_user_information],
)