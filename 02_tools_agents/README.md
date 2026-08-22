# Tool Agent — ADK

This example demonstrates how to extend a Google Agent Development Kit (ADK) agent with **custom function tools**.

Instead of relying only on the LLM's existing knowledge, the agent can call Python functions to retrieve **real-time weather data** from an external API.

---

## 🎯 What is a Tool Agent?

A Tool Agent extends a basic LLM agent by giving it additional capabilities through tools.

A normal LLM interaction looks like:

```text
User
 ↓
LLM
 ↓
Response
```

A tool-enabled agent can interact with external systems:

```text
User
 ↓
Agent
 ↓
LLM
 ↓
Tool
 ↓
External API
 ↓
Tool Result
 ↓
LLM
 ↓
Response
```

The important concept is that the **LLM decides when a tool is useful and invokes it when necessary**.

---

## 🛠️ What This Example Builds

This project creates a weather agent capable of answering questions about **current weather conditions**.

For example:

```text
User:
What's the current weather in Meerut?
```

The agent can:

1. Identify the city.
2. Find the city's coordinates.
3. Call the weather tool.
4. Retrieve current weather data from Open-Meteo.
5. Use the result to generate a natural-language response.

Example:

```text
The current weather in Meerut is mainly clear
with a temperature of 26.7°C.
```

---

## 🧩 Key Components

### 1. Agent

The ADK `Agent` is responsible for understanding the user's request and deciding whether a tool is required.

```python
root_agent = Agent(
    model="gemini-flash-latest",
    name="weather_agent",
    description="An assistant that provides current weather information.",
    instruction="
     You are a helpful weather assistant.
    When the user asks about the current weather:
    1. Identify the city from the user's question.
    2. Use get_coordinates to find the city's latitude and longitude.
    3. Use get_weather with those coordinates.
    4. Explain the current weather clearly.
    5. Do not invent weather information.
    6. If the user specifies Fahrenheit, use Fahrenheit.
       Otherwise use Celsius.
    For questions unrelated to weather, answer normally.",
    tools=[
        get_coordinates,
        get_weather,
    ],
)
```

---

### 2. Custom Function Tools

This example uses two custom Python functions as tools.

#### `get_coordinates()`

Converts a city name into geographical coordinates.

```text
City
 ↓
get_coordinates()
 ↓
Latitude + Longitude
```

For example:

```text
Meerut
 ↓
Latitude: ...
Longitude: ...
```

The tool uses the Open-Meteo Geocoding API.

---

#### `get_weather()`

Uses latitude and longitude to retrieve current weather information.

```text
Latitude + Longitude
 ↓
get_weather()
 ↓
Open-Meteo Forecast API
 ↓
Current weather data
```

The tool retrieves information such as:

* Temperature
* Apparent temperature
* Relative humidity
* Precipitation
* Wind speed
* Weather condition

---

## 🌐 External API

This project uses **Open-Meteo** for weather and geocoding data.

Open-Meteo provides weather forecast and geocoding APIs that can be accessed using HTTP requests.

The agent itself does not directly communicate with the weather API.

Instead:

```text
Agent
 ↓
Python Tool
 ↓
Open-Meteo API
 ↓
Python Tool
 ↓
Agent
```

This separation is an important part of the tool architecture.

---

## 📁 Project Structure

```text
02_tool_agent/
│
├── .env
├── .env.example
├── __init__.py
│
└── weather_agent/
    ├── __init__.py
    └── agent.py
```

> Your exact folder structure may differ depending on how the project was created with ADK. Keep the folder containing `agent.py` as the ADK agent package.

---

## 🔑 Environment Setup

This example uses the virtual environment created for the main repository.

From the repository root:

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
.venv\Scripts\activate.bat
```

### macOS / Linux

```bash
source .venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 API Key

Create a `.env` file for the agent and add your Google API key:

```env
GOOGLE_API_KEY=your_api_key_here
```

Never commit `.env` or your API key to GitHub.

Make sure `.env` is included in `.gitignore`.

---

## ▶️ Running the Agent

Navigate to the directory containing the agent package.

For example:

```powershell
cd 02_tool_agent
```

Then run:

```powershell
adk run tool_agent
```

You should see an interactive terminal similar to:

```text
Running agent tool_agent, type exit to exit.

[user]:
```

---

## 🧪 Example Prompts

Try asking:

```text
What's the current weather in Meerut?
```

```text
What's the current weather in Delhi?
```

```text
What's the current weather in Tokyo?
```

```text
What's the current weather in London in Fahrenheit?
```

You can also test whether the agent knows when **not** to use the weather tools:

```text
Explain recursion in simple terms.
```

The agent should answer the general question without needing weather data.

---

## 🔄 Tool Execution Flow

For:

```text
What's the current weather in Meerut?
```

the execution conceptually looks like:

```text
                    User
                      │
                      ▼
                 Gemini Agent
                      │
                      ▼
              Identify city
                      │
                      ▼
        get_coordinates("Meerut")
                      │
                      ▼
             Latitude / Longitude
                      │
                      ▼
          get_weather(latitude, longitude)
                      │
                      ▼
                Open-Meteo
                      │
                      ▼
             Current Weather
                      │
                      ▼
                 Gemini Agent
                      │
                      ▼
              Final Response
```

---

## 🧠 What I Learned

This example demonstrates several important Agentic AI concepts:

### Agent vs. Tool

The LLM does not need a tool for every question.

For example:

```text
"Explain recursion."
```

The LLM can answer directly.

But:

```text
"What's the current weather in Meerut?"
```

requires current external information.

The agent can therefore use:

```text
get_coordinates()
        ↓
get_weather()
```

---

### Why Use a Tool?

The purpose of a tool is to give the agent a capability that the LLM cannot reliably provide by itself.

Examples:

```text
LLM
 │
 ├── Calculator
 ├── Weather API
 ├── Web Search
 ├── Database
 ├── GitHub API
 └── Custom Application API
```

The LLM provides reasoning and language understanding, while tools provide access to external capabilities and data.

---

## ⚠️ Important Design Lesson

An agent is **not always necessary**.

For a simple weather application, this is perfectly valid:

```text
User
 ↓
Application Code
 ↓
Weather API
 ↓
Response
```

An agent becomes useful when the workflow is dynamic.

For example:

```text
User:
What's the weather in Delhi,
and should I go for a run?

        ↓

Agent
        ↓
get_coordinates()
        ↓
get_weather()
        ↓
Analyze result
        ↓
Generate recommendation
```

The agent can determine which capabilities are required instead of following one completely hard-coded path.

---

## 📚 Concepts Covered

* Google ADK `Agent`
* Custom function tools
* Function docstrings
* Tool parameters
* Tool return values
* LLM tool selection
* External REST APIs
* JSON responses
* Geocoding
* Current weather data
* Agent + external system integration

---

## 📖 Resources

* [Google ADK Documentation](https://google.github.io/adk-docs/)
* [ADK Function Tools](https://google.github.io/adk-docs/tools/function-tools/)
* [ADK Tools](https://google.github.io/adk-docs/tools/)
* [Open-Meteo Documentation](https://open-meteo.com/en/docs)
* [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api)

---

## 👨‍💻 Author

**Harsh Chauhan**

* Learning Journey: **Agentic AI with Google ADK**
* Example: **02 — Tool Agent**
* Started: **2026**

> Learning by building, experimenting, and understanding Agentic AI from the ground up.

---

**Part of the [ADK from Zero](../README.md) learning journey. 🚀**
