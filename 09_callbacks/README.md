# 09 — Callbacks in Google ADK

This project demonstrates how to use **Callbacks in Google's Agent Development Kit (ADK)** to observe, customize, and control agent execution.

Callbacks allow us to execute custom Python functions at specific points in an agent's lifecycle. They can be used for logging, state management, request validation, content filtering, modifying model responses, modifying tool arguments, blocking tool execution, and processing tool results.

---

## What I Learned

In this project, I explored three major callback levels in ADK:

```text
Agent Callbacks
      ↓
Model Callbacks
      ↓
Tool Callbacks
```

The main idea is to understand **when callbacks execute and how they can influence normal agent execution**.

---

## Callback Execution Flow

The overall execution can be understood as:

```text
User Request
     │
     ▼
┌─────────────────────┐
│ Before Agent        │
│ Callback            │
└──────────┬──────────┘
           │
           ▼
        Agent
           │
           ▼
┌─────────────────────┐
│ Before Model        │
│ Callback            │
└──────────┬──────────┘
           │
           ▼
          LLM
           │
           ▼
┌─────────────────────┐
│ After Model         │
│ Callback            │
└──────────┬──────────┘
           │
           ▼
      Tool Decision
           │
           ▼
┌─────────────────────┐
│ Before Tool         │
│ Callback            │
└──────────┬──────────┘
           │
           ▼
          Tool
           │
           ▼
┌─────────────────────┐
│ After Tool          │
│ Callback            │
└──────────┬──────────┘
           │
           ▼
        Response
           │
           ▼
┌─────────────────────┐
│ After Agent         │
│ Callback            │
└─────────────────────┘
```

---

# Project Structure

```text
09_callback/
│
├── 01_before_after_agent/
│   └── agent.py
│
├── 02_before_after_model/
│   └── agent.py
│
├── 03_before_after_tool/
│   └── agent.py
│
└── README.md
```

> The exact filenames may vary depending on the ADK Crash Course structure being followed.

---

# 01 — Before and After Agent Callbacks

The first example demonstrates:

```python
before_agent_callback
after_agent_callback
```

These callbacks run before and after the agent executes.

### Before Agent

The callback:

* Logs when the agent starts
* Stores the agent name in session state
* Maintains a request counter
* Records the request start time
* Prints execution information

Example state:

```python
{
    "agent_name": "SimpleChatBot",
    "request_counter": 1,
    "request_start_time": ...
}
```

### After Agent

The callback:

* Detects when the agent has finished
* Reads the request counter
* Calculates execution duration
* Logs completion information

The execution time is calculated using:

```python
duration = (
    datetime.now() - state["request_start_time"]
).total_seconds()
```

### What I Learned

The important concept from this example is:

```python
return None
```

Returning `None` tells ADK:

> Continue with the normal agent execution.

---

# 02 — Before and After Model Callbacks

The second example demonstrates:

```python
before_model_callback
after_model_callback
```

These callbacks operate around the LLM interaction.

---

## Before Model Callback

The callback receives:

```python
callback_context
llm_request
```

The `llm_request` contains information about the request that is going to be sent to the model.

The callback:

* Reads the current agent state
* Identifies the latest user message
* Logs the model request
* Stores the user message in state
* Checks for inappropriate content
* Can block the model request

### Content Filtering

The example checks whether the user's message contains:

```text
sucks
```

If it does, the callback returns an `LlmResponse` instead of `None`.

```text
User Request
     │
     ▼
Before Model Callback
     │
     ├── Allowed ──────► LLM
     │
     └── Blocked ──────► Custom LlmResponse
```

This demonstrates an important callback capability:

> A `before_model_callback` can intercept a model request and provide an alternative response instead of allowing the model call to continue.

---

## After Model Callback

The `after_model_callback` receives the model's response.

The example extracts the generated text and applies replacements:

```python
{
    "problem": "challenge",
    "difficult": "complex"
}
```

For example:

```text
Original:
This problem is difficult.

Modified:
This challenge is complex.
```

The callback creates a modified `LlmResponse` and returns it.

This demonstrates that callbacks can **inspect and modify model output**.

---

# 03 — Before and After Tool Callbacks

The third example demonstrates:

```python
before_tool_callback
after_tool_callback
```

These callbacks operate around tool execution.

The example uses a simple tool:

```python
get_capital_city(country)
```

The tool contains a small country-to-capital mapping.

---

## Before Tool Callback

The callback receives:

```python
tool
args
tool_context
```

It can inspect and modify the arguments before the tool executes.

### Argument Modification

If the LLM provides:

```text
country = "Merica"
```

the callback changes it to:

```text
country = "United States"
```

The execution becomes:

```text
LLM
 │
 │ country = "Merica"
 ▼
Before Tool Callback
 │
 │ modifies argument
 ▼
country = "United States"
 │
 ▼
get_capital_city()
```

---

## Blocking Tool Execution

The callback also demonstrates how a tool call can be intercepted.

If the country is:

```text
restricted
```

the callback returns its own result:

```python
{
    "result": "Access to this information has been restricted."
}
```

The actual tool does not need to execute.

This demonstrates **tool-level control**.

---

# After Tool Callback

The `after_tool_callback` runs after the tool has executed.

It receives the original tool response and can inspect or modify it.

For example, when the tool returns:

```python
{
    "result": "Washington, D.C."
}
```

the callback modifies it to:

```python
{
    "result": "Washington, D.C. (Note: This is the capital of the USA.)",
    "note_added_by_callback": True
}
```

This demonstrates how tool results can be processed before being passed further through the agent workflow.

---

# Important Callback Concept

One of the most important things learned in this project is the difference between:

```python
return None
```

and returning a replacement response.

### `return None`

```text
Continue normal execution
```

Example:

```python
def before_model_callback(...):
    # inspect request
    return None
```

Flow:

```text
Callback
   │
   ▼
LLM executes normally
```

### Return a replacement

For example:

```python
return LlmResponse(...)
```

Flow:

```text
Callback
   │
   ▼
Replacement response
   │
   X
LLM call skipped
```

Similarly, a `before_tool_callback` can return a replacement tool result and prevent the actual tool from running.

---

# What This Project Demonstrates

| Callback                | Purpose                                                |
| ----------------------- | ------------------------------------------------------ |
| `before_agent_callback` | Observe/control agent before execution                 |
| `after_agent_callback`  | Process information after agent execution              |
| `before_model_callback` | Inspect, validate, filter, or intercept model requests |
| `after_model_callback`  | Inspect or modify model responses                      |
| `before_tool_callback`  | Validate, modify, or block tool execution              |
| `after_tool_callback`   | Inspect or modify tool results                         |

---

# Key Concepts

Through this project, I practiced:

* ADK callback lifecycle
* Agent callbacks
* Model callbacks
* Tool callbacks
* `CallbackContext`
* `ToolContext`
* `LlmRequest`
* `LlmResponse`
* Session state
* Request counters
* Execution-time measurement
* Request logging
* Content filtering
* Model-response modification
* Tool-argument modification
* Tool execution interception
* Tool-result modification
* Returning `None` to continue execution
* Returning replacement responses to override normal behavior

---

# Main Takeaway

Callbacks provide **control points inside the agent execution lifecycle**.

They can be summarized as:

```text
OBSERVE
   ↓
Inspect what is happening

CUSTOMIZE
   ↓
Modify requests, arguments, responses, or results

CONTROL
   ↓
Allow, block, skip, or replace execution
```

The main lesson from this project is:

> **Callbacks allow an ADK application to observe, customize, and control what happens before and after agents, models, and tools execute.**

---

# Learning Progression

This project follows the progression:

```text
Agent Callback
      ↓
Model Callback
      ↓
Tool Callback
      ↓
State + Callback
      ↓
Request Filtering
      ↓
Response Modification
      ↓
Tool Control
```

This provides a foundation for building more advanced agent systems with validation, guardrails, logging, monitoring, and controlled tool execution.

---

## Reference

This project is based on the callback concepts and examples from the **Google Agent Development Kit (ADK) Crash Course** and ADK documentation.

* Google ADK documentation
* ADK Callbacks
* Before/After Agent Callbacks
* Before/After Model Callbacks
* Before/After Tool Callbacks
