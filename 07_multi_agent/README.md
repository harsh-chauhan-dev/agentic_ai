# Multi-Agent Systems in ADK

This example demonstrates how to build a **multi-agent system using Google's Agent Development Kit (ADK)**, where a manager agent delegates tasks to specialized agents based on the user's request.

The project also demonstrates **multiple models, custom Python tools, built-in ADK tools, agent delegation, and session state**.

## What is a Multi-Agent System?

A Multi-Agent System is an architecture where multiple specialized AI agents collaborate to solve different parts of a problem.

Instead of creating one agent responsible for everything, responsibilities are divided between specialized agents.

For example:

```text
                         User
                           |
                           v
                    +-------------+
                    | Root Agent  |
                    |   Manager   |
                    +------+------+
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
       Stock Analyst   News Analyst   Funny Nerd
             |             |             |
             v             v             v
          yfinance    Google Search   Custom Tool
```

The root agent acts as the **manager/orchestrator** and delegates requests to the appropriate specialist.

## Project Structure

This project uses a root agent with multiple specialized agents:

```text
07_multi_agent/
|
├── manager/
│   ├── __init__.py
│   └── agent.py
|
├── sub_agents/
│   ├── __init__.py
│   ├── funny_nerd.py
│   ├── news_analyst.py
│   └── stock_analyst.py
|
├── .venv/
├── requirements.txt
└── README.md
```

### Important Components

### 1. Root Agent

The `manager` package contains the root agent.

The `agent.py` file defines:

```python
root_agent = Agent(...)
```

The root agent is responsible for deciding which specialized agent should handle a request.

### 2. Sub-agents

The `sub_agents` directory contains specialized agents.

Current agents:

```text
sub_agents/
├── funny_nerd.py
├── news_analyst.py
└── stock_analyst.py
```

Each agent has a specific responsibility.

### 3. Agent Imports

The manager imports the specialized agents:

```python
from sub_agents.funny_nerd import funny_nerd
from sub_agents.news_analyst import news_analyst
from sub_agents.stock_analyst import stock_analyst
```

The agents are then registered with the root agent:

```python
root_agent = Agent(
    name="root_agent",
    model="gemini-2.0-flash",
    description="Manager agent",
    instruction="Delegate tasks to the appropriate specialist.",
    sub_agents=[
        stock_analyst,
        news_analyst,
        funny_nerd,
    ],
)
```

## Multi-Agent Architecture

ADK provides different ways to compose agents.

This project demonstrates **sub-agent delegation** and **agent-as-a-tool** concepts.

### 1. Sub-Agent Delegation

The root agent can delegate a task directly to a specialized sub-agent using `sub_agents`.

```python
root_agent = Agent(
    name="root_agent",
    model="gemini-2.0-flash",
    description="Manager agent",
    instruction="""
    Delegate stock questions to stock_analyst.
    Delegate news questions to news_analyst.
    Delegate jokes to funny_nerd.
    """,
    sub_agents=[
        stock_analyst,
        news_analyst,
        funny_nerd,
    ],
)
```

The flow is:

```text
User
 |
 v
Root Agent
 |
 +----> Stock Analyst
 |
 +----> News Analyst
 |
 +----> Funny Nerd
```

In this architecture, the specialized agent takes responsibility for handling the delegated task.

### 2. Agent as a Tool

ADK also supports using an agent as a tool with `AgentTool`.

```python
from google.adk.tools.agent_tool import AgentTool

root_agent = Agent(
    name="root_agent",
    model="gemini-2.0-flash",
    description="Manager agent",
    instruction="Use specialized agents when necessary.",
    tools=[
        AgentTool(news_analyst),
    ],
)
```

The difference is that the sub-agent behaves like a tool and returns its result to the root agent.

```text
Root Agent
    |
    v
AgentTool
    |
    v
News Analyst
    |
    v
Result
    |
    v
Root Agent
    |
    v
Final Response
```

This gives the root agent more control over how the result is used.

## Agents in This Project

This example contains three specialized agents.

### 1. Stock Analyst

The `stock_analyst` handles stock market and stock price requests.

It uses a custom Python tool:

```python
get_stock_price()
```

The tool uses `yfinance` to retrieve stock information.

Workflow:

```text
User
 |
 v
Root Agent
 |
 v
Stock Analyst
 |
 v
get_stock_price()
 |
 v
yfinance
 |
 v
Stock Data
```

Example prompt:

```text
What is the current price of AAPL?
```

The tool returns structured information:

```json
{
    "status": "success",
    "ticker": "AAPL",
    "price": 200.50,
    "timestamp": "2026-08-27 13:30:00"
}
```

> **Note:** `yfinance` data may be delayed and should not be considered guaranteed exchange-grade real-time data.

### 2. News Analyst

The `news_analyst` handles current and recent news.

It uses the ADK `google_search` tool.

Workflow:

```text
User
 |
 v
Root Agent
 |
 v
News Analyst
 |
 v
google_search
 |
 v
Search Results
 |
 v
News Analysis
 |
 v
Response
```

Example prompt:

```text
What's the latest technology news?
```

For relative dates such as:

```text
today
yesterday
this week
```

the agent can use a current-time tool to establish the appropriate date before performing the search.

### 3. Funny Nerd

The `funny_nerd` agent generates jokes about technical and scientific topics.

It uses the custom tool:

```python
get_nerd_joke()
```

Supported topics include:

```text
Python
JavaScript
Java
Programming
Math
Physics
Chemistry
Biology
```

Example:

```text
Tell me a Python joke.
```

The tool also demonstrates ADK `ToolContext`:

```python
tool_context.state["last_joke_topic"] = topic
```

This stores information in the current session state.

## Tools

This project demonstrates both **built-in ADK tools** and **custom Python tools**.

### Built-in Tool

```python
google_search
```

Used by:

```text
news_analyst
```

### Custom Tool: Stock Price

```python
get_stock_price()
```

Uses:

```python
import yfinance
```

### Custom Tool: Nerd Joke

```python
get_nerd_joke()
```

Uses:

```python
ToolContext
```

to interact with session state.

## Multiple Models

One important concept demonstrated by this project is that agents can use different models.

For example:

```text
Root Agent
    |
    +---- Stock Analyst
    |        |
    |        +---- Gemini model
    |
    +---- News Analyst
    |        |
    |        +---- Gemini model
    |
    +---- Funny Nerd
             |
             +---- Gemini model
```

The model is configured independently for each agent:

```python
stock_analyst = Agent(
    name="stock_analyst",
    model="gemini-2.0-flash",
    ...
)
```

```python
news_analyst = Agent(
    name="news_analyst",
    model="gemini-3.5-flash",
    ...
)
```

```python
funny_nerd = Agent(
    name="funny_nerd",
    model="gemini-3.5-flash",
    ...
)
```

Using different models can allow an application to optimize for:

* Cost
* Latency
* Reasoning capability
* Task complexity
* Tool usage

## Agent Delegation Example

A stock request:

```text
User:
What is the current price of AAPL?

        |
        v

root_agent

        |
        v

stock_analyst

        |
        v

get_stock_price()

        |
        v

yfinance

        |
        v

Stock Price
```

A news request:

```text
User:
What's the latest AI news?

        |
        v

root_agent

        |
        v

news_analyst

        |
        v

google_search

        |
        v

News Results
```

A joke request:

```text
User:
Tell me a Python joke.

        |
        v

root_agent

        |
        v

funny_nerd

        |
        v

get_nerd_joke()

        |
        v

Joke
```

## ToolContext and Session State

The `funny_nerd` agent demonstrates how tools can interact with ADK session state.

Example:

```python
def get_nerd_joke(
    topic: str,
    tool_context: ToolContext
) -> dict:

    tool_context.state["last_joke_topic"] = topic

    return {
        "status": "success",
        "topic": topic
    }
```

The flow is:

```text
Tool
 |
 v
ToolContext
 |
 v
Session State
```

This allows tools to read or modify information associated with the current session.

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If `yfinance` is not included in `requirements.txt`:

```bash
python -m pip install yfinance
```

Verify the installation:

```bash
python -c "import yfinance; print(yfinance.__version__)"
```

## Environment Variables

Configure the API key required by your Google/Gemini setup.

Example:

```env
GOOGLE_API_KEY=your_api_key
```

Never commit API keys to GitHub.

Add the following to `.gitignore`:

```text
.env
.venv/
__pycache__/
```

## Running the Example

Run ADK from the directory containing the root agent package.

For this project:

```bash
adk web
```

The ADK web interface should open at the URL displayed in the terminal, usually:

```text
http://localhost:8000
```

Select the `manager` / root agent from the interface and start chatting.

## Important: Running Location

Run:

```bash
adk web
```

from:

```text
07_multi_agent/
```

not from inside:

```text
manager/
```

or:

```text
sub_agents/
```

Correct:

```text
07_multi_agent/
    ├── manager/
    ├── sub_agents/
    └── README.md

    $ adk web
```

Incorrect:

```text
07_multi_agent/manager/

    $ adk web
```

## Troubleshooting

### `ImportError: cannot import name 'funny_nerd'`

Make sure `funny_nerd.py` defines:

```python
funny_nerd = Agent(...)
```

and that the import matches:

```python
from sub_agents.funny_nerd import funny_nerd
```

### `Import "yfinance" could not be resolved`

Make sure VS Code is using the project's virtual environment.

Select:

```text
Python: Select Interpreter
```

and choose:

```text
.venv\Scripts\python.exe
```

Verify:

```bash
python -c "import yfinance; print(yfinance.__version__)"
```

### Agent does not appear in ADK Web

Check:

* `adk web` is running from `07_multi_agent/`
* `manager/__init__.py` imports `agent`
* `manager/agent.py` defines `root_agent`
* Sub-agent imports are correct
* Agent variable names match the import statements

## Example Prompts

Try the following prompts:

### Stock

```text
What is the current price of AAPL?
```

### News

```text
What's the latest technology news?
```

### Nerd Joke

```text
Tell me something funny about Python.
```

### State

```text
Tell me a Python joke.
```

Then ask another question that can make use of the current conversation context.

## Key Concepts

This example demonstrates:

* Multi-agent architecture
* Root/manager agents
* Specialized sub-agents
* Agent delegation
* Agent-as-a-tool
* Multiple LLM models
* Custom Python tools
* Built-in ADK tools
* `ToolContext`
* Session state
* External data integration
* `yfinance`
* Google Search
* Tool error handling

## Additional Resources

* [ADK Multi-Agent Systems Documentation](https://google.github.io/adk-docs/agents/multi-agent-systems/)
* [ADK Agents Documentation](https://google.github.io/adk-docs/agents/)
* [ADK Tools Documentation](https://google.github.io/adk-docs/tools/)
* [Agent as a Tool](https://google.github.io/adk-docs/tools/function-tools/#3-agent-as-a-tool)
* [ADK Sessions & State](https://google.github.io/adk-docs/sessions/)
* [yfinance Documentation](https://github.com/ranaroussi/yfinance)


## 👨‍💻 Author

**Harsh Chauhan**

BCA Student | Software Developer | AI & Agentic AI Enthusiast

GitHub:
https://github.com/harsh-chauhan-dev
