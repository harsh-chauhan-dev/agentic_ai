# Stateful Multi-Agent Customer Service System

A hands-on Google ADK project demonstrating how multiple specialized agents can work together while sharing and modifying **session state**.

The system simulates a customer-service platform for an online course business. A main Customer Service Agent delegates requests to specialized agents for sales, orders/refunds, and course support.

---

## 🚀 What This Project Demonstrates

This project focuses on **stateful multi-agent systems** using the Google Agent Development Kit (ADK).

It demonstrates:

* Multi-agent delegation
* Specialized sub-agents
* ADK `Runner`
* `InMemorySessionService`
* Session creation and management
* Shared session state
* State mutation through `ToolContext`
* State-dependent agent behavior
* Async ADK APIs
* Tool-based workflows
* Purchase and refund workflows
* Agent-to-agent transfers
* Custom interaction history

---

## 🧠 Core Concept

A multi-agent system can divide responsibilities between specialized agents.

Instead of one large agent handling every request:

```text
                         User
                           │
                           ▼
                 Customer Service Agent
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
       Sales Agent    Order Agent    Course Support
             │             │             │
             ▼             ▼             ▼
        Purchase       Refund /       Course Help
          Tool        Order History
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                    Session State
```

The agents share information through the ADK session state.

For example, after purchasing a course:

```text
purchased_courses
        │
        ▼
ai_marketing_platform
```

The Course Support Agent can then use that state to determine whether the user owns the course.

---

# 🏗️ Project Architecture

```text
08_stateful_multi_agent/
│
├── customer_service_agent/
│   ├── __init__.py
│   ├── agent.py
│   │
│   └── sub_agents/
│       ├── __init__.py
│       ├── sales_agent.py
│       ├── order_agent.py
│       └── course_support.py
│
├── main.py
├── utils.py
├── .env
└── README.md
```

### Main Components

| Component                | Responsibility                                  |
| ------------------------ | ----------------------------------------------- |
| `customer_service_agent` | Main entry-point agent and request router       |
| `sales_agent`            | Course information and purchases                |
| `order_agent`            | Purchase history and refunds                    |
| `course_support`         | Course-specific support                         |
| `main.py`                | Session, runner, and CLI application            |
| `utils.py`               | State display and interaction-history utilities |

---

# 🤖 Agents

## 1. Customer Service Agent

The Customer Service Agent is the main entry point.

Its job is to understand the user's request and transfer it to the appropriate specialized agent.

Example:

```text
User:
I want to buy the AI Marketing Platform course.

Customer Service Agent
        ↓
Sales Agent
```

---

## 2. Sales Agent

The Sales Agent handles:

* Course information
* Course pricing
* Course purchases
* Duplicate purchase detection

It uses the `purchase_course()` tool to modify session state.

Example state:

```python
tool_context.state["purchased_courses"] = new_purchased_courses
```

---

## 3. Order Agent

The Order Agent handles:

* Purchase history
* Order information
* Refund requests

The refund workflow modifies:

```text
purchased_courses
```

and removes the refunded course from the user's state.

---

## 4. Course Support Agent

The Course Support Agent handles course-specific questions.

It can use the user's session state to determine whether the user has purchased the course.

Example:

```text
User:
Help me with the NextJS section.

        ↓

Course Support Agent

        ↓

Checks purchased_courses

        ↓

Provides course-specific support
```

---

# 🗃️ Session State

The most important concept in this project is **session state**.

The initial state contains:

```python
initial_state = {
    "user_name": "Harsh Chauhan",
    "purchased_courses": [],
    "interaction_history": [],
}
```

### State Structure

```text
Session State
│
├── user_name
│
├── purchased_courses
│
└── interaction_history
```

### `user_name`

Stores the user's name.

```python
"user_name": "Harsh Chauhan"
```

### `purchased_courses`

Stores courses purchased by the user.

Initially:

```python
"purchased_courses": []
```

After purchasing:

```python
"purchased_courses": [
    {
        "id": "ai_marketing_platform",
        "purchase_date": "..."
    }
]
```

### `interaction_history`

Stores application-level interaction information such as:

```text
user_query
agent_response
purchase_course
refund_course
```

---

# 🔄 Stateful Workflow

The state changes throughout the conversation.

## Step 1 — Initial State

```text
purchased_courses = []
```

---

## Step 2 — Purchase

User:

```text
I want to purchase the AI Marketing Platform course.
```

The request is transferred to the Sales Agent.

The purchase tool updates:

```text
purchased_courses
        ↓
ai_marketing_platform
```

---

## Step 3 — State Persists

The user can ask:

```text
Do I own the AI Marketing Platform course?
```

The agent can read the existing session state.

---

## Step 4 — Course Support

User:

```text
Can you explain the NextJS API routes section?
```

The request can be transferred to Course Support.

The agent can see:

```text
purchased_courses
    └── ai_marketing_platform
```

and provide course-specific assistance.

---

## Step 5 — Refund

User:

```text
I want a refund for the AI Marketing Platform course.
```

The Order Agent executes the refund workflow.

The state becomes:

```text
purchased_courses = []
```

---

# 🔀 Example Agent Flow

```text
User
 │
 │ "I want to purchase the course"
 ▼
Customer Service
 │
 │ transfer
 ▼
Sales Agent
 │
 │ purchase_course()
 ▼
Session State
 │
 └── purchased_courses
       └── ai_marketing_platform
```

Later:

```text
User
 │
 │ "Help me with NextJS"
 ▼
Customer Service
 │
 │ transfer
 ▼
Course Support
 │
 │ reads session state
 ▼
purchased_courses
 │
 └── ai_marketing_platform
```

---

# 🧪 Testing

The project was tested through an interactive CLI conversation.

### Purchase

```text
I want to purchase the AI Marketing Platform course
```

Expected:

```text
Successfully purchased the course
```

And:

```text
purchased_courses:
    ai_marketing_platform
```

### Duplicate Purchase

```text
I want to purchase the AI Marketing Platform course again.
```

Expected:

```text
You already own the course.
```

### Purchase History

```text
Show my purchase history.
```

Expected:

```text
Order Agent
    ↓
Purchase information
```

### Course Support

```text
Can you explain the NextJS API routes section in detail?
```

Expected:

```text
Customer Service
        ↓
Course Support
        ↓
Course-specific response
```

### Refund

```text
I want a refund for my course.
```

Expected:

```text
purchased_courses = []
```

### State Verification

After the refund:

```text
Do I still own the course?
```

Expected:

```text
No
```

---

# ⚙️ Requirements

* Python 3.10+
* Google ADK
* Google Gemini API key
* `python-dotenv`

The project was developed and tested with:

```text
google-adk 2.8.0
```

---

# 🔐 Environment Setup

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
```

Do **not** commit your `.env` file.

Add it to `.gitignore`:

```text
.env
.venv/
__pycache__/
```

---

# ▶️ Running the Project

Activate your virtual environment:

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install google-adk python-dotenv
```

Run:

```powershell
python main.py
```

You should see:

```text
Created new session: <session-id>

Welcome to Customer Service Chat!
Type 'exit' or 'quit' to end the conversation.
```

---

# 💡 Example Conversation

```text
You: What courses do you offer?

You: I want to purchase the AI Marketing Platform course.

You: Show my purchase history.

You: Can you help me with the NextJS section?

You: I want a refund for my course.

You: Do I still own the course?
```

This sequence demonstrates the complete state lifecycle:

```text
Initial State
     ↓
Purchase
     ↓
State Updated
     ↓
Read State
     ↓
Course Support
     ↓
Refund
     ↓
State Updated Again
```

---

# ⚠️ Notes

The project uses `InMemorySessionService`, so session data exists only while the application is running.

Restarting:

```powershell
python main.py
```

creates a new session and resets the initial state.

For a production application, persistent storage would be required.

---

# 📚 Key ADK Concepts

This project helped demonstrate several important ADK concepts:

### Session

Represents the ongoing conversation and its state.

### State

Stores information that agents and tools can access during the session.

### ToolContext

Allows tools to read and modify session state.

Example:

```python
tool_context.state["purchased_courses"] = new_purchased_courses
```

### Runner

Connects the agent, application, and session service to execute the conversation.

### Multi-Agent Delegation

Allows a main agent to transfer a task to a specialized agent.

---

# 🎯 What I Learned From This Project

The main takeaway is that a multi-agent system becomes much more useful when agents can share **persistent context within a session**.

Instead of every agent independently trying to determine what happened previously, they can work with shared state:

```text
             Shared Session State
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
      Sales        Orders       Support
        │            │            │
        └────────────┼────────────┘
                     ▼
             User's Current State
```

This creates a foundation for building more advanced agentic applications such as:

* Customer-support automation
* E-commerce assistants
* Personal AI assistants
* Workflow automation
* Multi-agent business systems
* AI-powered SaaS applications

---

# 🔗 Resources

* [Google Agent Development Kit Documentation](https://google.github.io/adk-docs/)
* [Google ADK GitHub](https://github.com/google/adk-python)
* [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs)

---


