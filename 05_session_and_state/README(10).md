# 05 - Sessions and State with Google ADK

A practical Google Agent Development Kit (ADK) project demonstrating how
**sessions, conversation events, and state** work in an AI agent.

This project was built as part of the Agentic AI learning path and
focuses on one of the most important concepts in ADK: giving an agent a
structured place to maintain information across a conversation.

------------------------------------------------------------------------

## What is Google ADK?

**Google Agent Development Kit (ADK)** is a framework for building AI
agents with capabilities such as:

- Agents and instructions
- Tools
- Sessions
- State
- Callbacks
- Multi-agent workflows
- Evaluation
- Observability

This project focuses specifically on **Sessions and State**.

------------------------------------------------------------------------

# 1. What is a Session?

A **Session** represents one continuous interaction between a user and
an agent.

You can think of a session as a conversation container.

``` text
User
  │
  ▼
Session
  │
  ├── User messages
  ├── Agent responses
  ├── Tool calls
  ├── Events
  └── State
```

A session normally has identifiers such as:

``` text
user_id
session_id
app_name
```

For example:

``` text
user_id    = harsh
session_id = session_001
```

If multiple messages use the same session, ADK can associate those
interactions with the same conversation.

------------------------------------------------------------------------

# 2. What is State?

**State is structured information associated with a session.**

For example:

``` python
{
    "user_name": "Harsh",
    "learning_topic": "Agentic AI",
    "favorite_language": "Python"
}
```

State is different from simply having a conversation history.

### Conversation

``` text
User: My name is Harsh.
Agent: Nice to meet you!

User: I am learning Agentic AI.
Agent: Great!
```

### State

``` python
{
    "user_name": "Harsh",
    "learning_topic": "Agentic AI"
}
```

Conversation history contains events and messages.

State contains structured application data that the agent can use.

------------------------------------------------------------------------

# 3. Session vs State

A useful mental model:

``` text
                    SESSION
                       │
          ┌────────────┴────────────┐
          │                         │
       EVENTS                    STATE
          │                         │
          │                   ┌─────┴─────┐
          │                   │           │
    User messages         user_name   learning_topic
    Agent responses
    Tool calls
```

### Session

Answers:

> "Which conversation does this interaction belong to?"

### State

Answers:

> "What structured information are we currently keeping for this
> conversation?"

------------------------------------------------------------------------

# 4. Why State Does Not Automatically Change

One of the most important lessons from this project:

Giving the LLM an instruction such as:

``` text
Remember the user's name.
```

does **not** automatically execute:

``` python
session.state["user_name"] = "Harsh"
```

The model can say:

``` text
"I'll remember your name."
```

while the actual state remains:

``` text
user_name: "Unknown"
```

State mutation needs an explicit application mechanism.

In this project, we use an ADK tool with `ToolContext`.

------------------------------------------------------------------------

# 5. Updating State with ToolContext

The project contains a tool similar to:

``` python
from google.adk.tools import ToolContext


def save_user_information(
    tool_context: ToolContext,
    user_name: str | None = None,
    learning_topic: str | None = None,
    favorite_language: str | None = None,
) -> dict:

    if user_name:
        tool_context.state["user_name"] = user_name

    if learning_topic:
        tool_context.state["learning_topic"] = learning_topic

    if favorite_language:
        tool_context.state["favorite_language"] = favorite_language

    return {
        "status": "success"
    }
```

The important line is:

``` python
tool_context.state["user_name"] = user_name
```

The tool receives access to the current state through `ToolContext` and
updates it.

Conceptually:

``` text
User
 │
 │ "My name is Harsh"
 ▼
LLM Agent
 │
 │ decides to use tool
 ▼
save_user_information()
 │
 ▼
ToolContext
 │
 ▼
tool_context.state
 │
 ▼
Session State
```

------------------------------------------------------------------------

# 6. What This Project Does

This project implements a simple **Personal Assistant Agent**.

The agent can maintain information such as:

``` text
user_name
learning_topic
favorite_language
```

Example interaction:

``` text
User:
My name is Harsh.

Agent:
Nice to meet you, Harsh!

User:
I am learning Agentic AI.

Agent:
Great! I'll remember that.

User:
My favorite programming language is Python.

Agent:
Got it!
```

The state can then become:

``` python
{
    "user_name": "Harsh",
    "learning_topic": "Agentic AI",
    "favorite_language": "Python"
}
```

The agent can later use this state:

``` text
User:
What do you remember about me?

Agent:
Your name is Harsh, you're learning Agentic AI,
and your favorite programming language is Python.
```

------------------------------------------------------------------------

# 7. Project Architecture

``` text
                    ADK WEB UI
                        │
                        ▼
                   User Message
                        │
                        ▼
                  ADK Runner
                        │
                        ▼
                     Agent
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
             LLM                Tools
                                  │
                                  ▼
                             ToolContext
                                  │
                                  ▼
                              Session State
                                  │
                ┌─────────────────┼─────────────────┐
                ▼                 ▼                 ▼
           user_name       learning_topic    favorite_language
```

------------------------------------------------------------------------

# 8. ADK Web Interface

The project was tested using the ADK Web development interface.

Start it with:

``` powershell
adk web --port 8000
```

The browser provides a chat interface for interacting with the agent.

The ADK Web interface also exposes useful debugging information such as:

-   Events
-   State
-   Artifacts
-   Evals
-   Traces

This makes it much easier to understand what happens internally during
an agent execution.

------------------------------------------------------------------------

# 9. State Panel

The ADK Web State panel allows us to inspect the current state.

Initially:

``` text
user_name: "Unknown"
learning_topic: "Unknown"
favorite_language: "Unknown"
```

After the user provides information:

``` text
user_name: "Harsh"
learning_topic: "Agentic AI"
favorite_language: "Python"
```

This gives a visual way to verify that the state was actually modified.

------------------------------------------------------------------------

# 10. Events vs State

These concepts should not be confused.

## Events

Events represent things that happened during the interaction.

Example:

``` text
User message
     ↓
Agent response
     ↓
Tool call
     ↓
Tool result
```

## State

State represents structured information currently associated with the
session.

Example:

``` python
{
    "user_name": "Harsh",
    "learning_topic": "Agentic AI"
}
```

A simple comparison:

  -----------------------------------------------------------------------
  Concept                             Purpose
  ----------------------------------- -----------------------------------
  Session                             Container for one conversation

  Event                               Records something that happened

  State                               Structured information maintained
                                      for the session

  ToolContext                         Gives a tool access to agent
                                      execution context, including state
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 11. InMemorySessionService

The manual version of this project uses:

``` python
from google.adk.sessions import InMemorySessionService
```

This stores session information in memory.

Example:

``` python
session_service = InMemorySessionService()
```

Then:

``` python
session = await session_service.create_session(
    app_name="sessions_and_state",
    user_id="harsh",
    session_id="session_001",
)
```

This is useful for:

-   Learning
-   Development
-   Testing
-   Prototyping

But it is not a production database.

If the Python process is restarted, in-memory session data can be lost.

For production systems, session persistence should use an appropriate
persistent session service/storage option.

------------------------------------------------------------------------

# 12. Manual Runner vs ADK Web

This project was tested in two ways.

## Manual approach

``` text
main.py
   │
   ▼
SessionService
   │
   ▼
Runner
   │
   ▼
Agent
```

This approach is useful for understanding the ADK Python APIs directly.

## ADK Web approach

``` text
Browser
   │
   ▼
ADK Web
   │
   ▼
Runner / Session
   │
   ▼
Agent
```

The Web UI provides a much easier environment for interactively testing
sessions, state, events, and traces.

------------------------------------------------------------------------

# 13. API Key

The project uses the Gemini API.

A `.env` file is used for local configuration:

``` env
GOOGLE_API_KEY=your_api_key
```

Never commit the real API key to GitHub.

Recommended `.gitignore`:

``` text
.env
.venv/
__pycache__/
```

------------------------------------------------------------------------

# 14. API Errors and Limits

During development, the project encountered a Gemini API:

``` text
503 UNAVAILABLE
```

The API response indicated that the model was temporarily experiencing
high demand.

This is different from an invalid API key.

Possible API failures include:

``` text
401 / authentication errors
429 / quota or rate-limit errors
500 / server errors
503 / temporary service unavailability
```

A production agent should handle these failures gracefully instead of
crashing the entire application.

For example:

``` text
Gemini API
    │
    ├── Success ──────────► Agent response
    │
    ├── 429 ──────────────► Retry/backoff
    │
    ├── 503 ──────────────► Retry/backoff
    │
    └── Other error ──────► Handle/report error
```

------------------------------------------------------------------------

# 15. Example State Lifecycle

The complete lifecycle looks like:

``` text
1. Create session
        ↓
2. Initialize state
        ↓
3. User sends message
        ↓
4. Agent processes message
        ↓
5. Agent decides to use a tool
        ↓
6. Tool receives ToolContext
        ↓
7. Tool updates state
        ↓
8. ADK records the state change
        ↓
9. Session contains updated state
        ↓
10. Future requests can use the state
```

------------------------------------------------------------------------

# 16. What I Learned From This Project

The biggest lessons from `05_session_and_state` are:

### 1. Session is not State

A session represents a conversation context.

State is structured information associated with that session.

### 2. Conversation memory is not automatically application state

An LLM seeing previous messages does not mean your application's state
dictionary has changed.

### 3. State mutation should be explicit

Use ADK mechanisms such as `ToolContext` to intentionally modify state.

### 4. ADK Web is extremely useful for debugging

The State, Events, and Traces views make agent execution much easier to
understand.

### 5. In-memory sessions are for development

They are excellent for learning but should not be treated as durable
production storage.

------------------------------------------------------------------------

# 17. Technologies Used

-   Python
-   Google ADK
-   Gemini API
-   `google-adk`
-   `python-dotenv`
-   Async Python
-   ADK Web
-   `InMemorySessionService`
-   `Runner`
-   `ToolContext`

------------------------------------------------------------------------

# 18. Run the Project

Create and activate the virtual environment:

``` powershell
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

``` powershell
pip install google-adk python-dotenv
```

Set the API key in `.env`:

``` env
GOOGLE_API_KEY=your_api_key
```

Run the terminal version:

``` powershell
python main.py
```

Run the ADK Web interface:

``` powershell
adk web --port 8000
```

Then open the local URL shown by ADK.

------------------------------------------------------------------------

# 19. Project Structure

``` text
05_session_and_state/
│
├── personal_assistant_agent/
│   ├── __init__.py
│   └── agent.py
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

### `agent.py`

Contains:

-   Agent definition
-   Agent instructions
-   State-aware behavior
-   `save_user_information` tool
-   `ToolContext` state updates

### `main.py`

Contains the manual runner/session experiment.

It demonstrates:

-   Session creation
-   `InMemorySessionService`
-   Runner
-   User interaction
-   Session IDs
-   State inspection

### `.env`

Stores the Gemini API key locally.

------------------------------------------------------------------------

# 20. Official Documentation

-   Google ADK documentation: https://google.github.io/adk-docs/
-   ADK Python documentation:
    https://google.github.io/adk-docs/api-reference/python/
-   ADK Sessions and State: https://google.github.io/adk-docs/sessions/
-   ADK Tools: https://google.github.io/adk-docs/tools/
-   ADK Web: https://google.github.io/adk-docs/get-started/quickstart/

------------------------------------------------------------------------

# Conclusion

`05_session_and_state` demonstrates the foundation of a **stateful AI
agent**.

The core idea is:

``` text
                    AI AGENT
                       │
                       ▼
                    SESSION
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
          EVENTS               STATE
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
               user_name   learning_topic  favorite_language
```

The agent does not simply generate text. It can operate within a
session, use structured state, call tools, and update information that
can be used by later interactions.

This is an important building block for more advanced Agentic AI systems
such as:

-   Personal assistants
-   Customer-support agents
-   Multi-turn workflows
-   Multi-agent systems
-   Task-management agents
-   Stateful automation
-   Long-running agent applications

**Next logical topic:** persistent sessions and more advanced state
management.
