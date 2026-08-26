# 06 — Persistent Storage Memory Agent

A Google ADK project demonstrating how to build an agent with **persistent session storage** using `DatabaseSessionService`, SQLite, SQLAlchemy, and `aiosqlite`.

The agent can remember user information and reminders even after the application is stopped and started again.

---

## 📌 What is Persistent Storage?

**Persistent storage** means storing data in a way that survives after an application stops or restarts.

For example, normal in-memory state might look like:

```text
Application starts
       ↓
State created
       ↓
User stores information
       ↓
Application stops
       ↓
State disappears
```

With persistent storage:

```text
Application starts
       ↓
Load state from database
       ↓
User stores information
       ↓
State saved to database
       ↓
Application stops
       ↓
Application starts again
       ↓
Previous state is restored
```

In this project, ADK stores session information in a SQLite database.

---

# 🧠 Session vs State vs Persistent Storage

These concepts are related but different.

| Concept                    | Meaning                                                                         |
| -------------------------- | ------------------------------------------------------------------------------- |
| **Session**                | Represents a conversation between a user and an agent                           |
| **State**                  | Data associated with that session                                               |
| **Persistent Storage**     | Storage that keeps the session/state beyond the lifetime of the running process |
| **DatabaseSessionService** | ADK session service that stores sessions using a database                       |

For example, this project stores:

```python
{
    "user_name": "Harsh",
    "reminders": [
        "study ADK",
        "study Computer Architecture"
    ]
}
```

The state is associated with an ADK session and persisted through the database-backed session service.

---

# 🏗️ Project Architecture

```text
                         User
                          │
                          ▼
                  ┌───────────────┐
                  │ Memory Agent  │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │  Agent Tools  │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │ ToolContext   │
                  │    State      │
                  └───────┬───────┘
                          │
                          ▼
              ┌────────────────────────┐
              │ DatabaseSessionService │
              └────────────┬───────────┘
                           │
                           ▼
                      SQLAlchemy
                           │
                           ▼
                       aiosqlite
                           │
                           ▼
                    ┌──────────────┐
                    │    SQLite    │
                    │              │
                    │ my_agent_    │
                    │ data.db      │
                    └──────────────┘
```

---

# 🚀 What This Project Does

The agent is a persistent reminder assistant.

It can:

* Remember the user's name
* Add reminders
* View reminders
* Update reminders
* Delete reminders
* Persist state across application restarts
* Restore an existing ADK session from SQLite

Example:

```text
User: My name is Harsh

Agent: Hi Harsh! I'll remember your name.
```

Then:

```text
User: Add a reminder to study ADK

Agent: Added reminder: study ADK
```

After completely stopping the application and starting it again:

```text
User: What is my name?

Agent: Your name is Harsh.
```

And:

```text
User: Show my reminders

1. study ADK
```

The information survives because it is stored through the database-backed session service.

---

# 📁 Project Structure

```text
06_persistent_storage/
│
├── memory_agent/
│   ├── __init__.py
│   └── agent.py
│
├── main.py
├── utils.py
├── requirements.txt
│
├── .gitignore
│
└── my_agent_data.db
```

> `my_agent_data.db` is generated locally and should not be committed to GitHub.

---

```text
                  Application Start
                         │
                         ▼
                  list_sessions()
                         │
              ┌──────────┴──────────┐
              │                     │
          Session exists?           No
              │                     │
             Yes                    ▼
              │              create_session()
              ▼                     │
       Continue session             │
              │                     │
              └──────────┬──────────┘
                         ▼
                    Run Agent
```

---

# 🧠 State Management

The agent uses `ToolContext` to access and modify session state.

For example:

```python
reminders = tool_context.state.get(
    "reminders",
    []
)
```

A new reminder is added:

```python
reminders.append(reminder)
```

Then the state is updated:

```python
tool_context.state["reminders"] = reminders
```

Because the session service is database-backed, the state can persist with the session.

---

# 🛠️ Available Tools

## `add_reminder`

Adds a reminder to the user's state.

```text
add_reminder("study ADK")
```

---

## `view_reminders`

Returns all stored reminders.

```text
view_reminders()
```

---

## `update_reminder`

Updates an existing reminder using its position.

```text
update_reminder(
    index=1,
    updated_text="study Computer Architecture"
)
```

---

## `delete_reminder`

Deletes a reminder.

```text
delete_reminder(
    index=1
)
```

---

## `update_user_name`

Updates the user's name in session state.

```text
update_user_name(
    name="Harsh"
)
```

---

# ⚡ Quick Start

## 1. Clone the repository

```bash
git clone https://github.com/harsh-chauhan-dev/agentic_ai.git
```

Navigate to:

```bash
cd agentic_ai/06_persistent_storage
```

---

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

---

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Configure Gemini API Key

Create:

```text
.env
```

Add:

```env
GOOGLE_API_KEY=your_api_key_here
```

Never commit `.env` to GitHub.

---

## 5. Run the agent

```powershell
python main.py
```

You should see:

```text
Welcome to Memory Agent Chat!

Your reminders will be remembered across conversations.

Type 'exit' or 'quit' to end the conversation.
```

---

# 🧪 Test Persistent Storage

## Test 1 — Store information

```text
You: My name is Harsh
```

Then:

```text
You: Add a reminder to study ADK
```

Then:

```text
You: Add a reminder to study Computer Architecture
```

View them:

```text
You: Show my reminders
```

Expected:

```text
1. study ADK
2. study Computer Architecture
```

---

## Test 2 — Restart the application

Exit:

```text
You: exit
```

Start again:

```powershell
python main.py
```

You should see:

```text
Continuing existing session: <session-id>
```

Then:

```text
You: What is my name?
```

Expected:

```text
Your name is Harsh.
```

And:

```text
You: Show my reminders
```

Expected:

```text
1. study ADK
2. study Computer Architecture
```

If the information is still available after restarting the application, persistent storage is working correctly.

---



---

# 🔐 Environment Variables

The API key should be stored in `.env`:

```env
GOOGLE_API_KEY=your_api_key_here
```

The following should **not** be committed:

```text
.env
.venv/
*.db
```

---

# 📚 Official Documentation

### Google Agent Development Kit

Official ADK documentation:

https://google.github.io/adk-docs/

### ADK Python Documentation

https://google.github.io/adk-docs/

### Google Agents CLI

Official Agents CLI documentation:

https://google.github.io/agents-cli/

The current Agents CLI documentation lists session storage options including in-memory and database-backed approaches.

### Agents CLI Authentication

Documentation for Gemini API-key authentication and other model authentication options:

https://google.github.io/agents-cli/guide/authentication/

Google's documentation notes that `GOOGLE_API_KEY` is accepted for Gemini API-key authentication.

### Agents CLI Manual Tutorial

Official hands-on tutorial for building and running ADK agents:

https://google.github.io/agents-cli/guide/hands-on-tutorial/

### Agents CLI Project Structure

Official project structure reference:

https://google.github.io/agents-cli/guide/project-structure/

---

## Author

**Harsh Chauhan**

BCA Student | Software Development & Agentic AI

GitHub:

https://github.com/harsh-chauhan-dev
