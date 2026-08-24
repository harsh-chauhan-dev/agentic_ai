# 04 — Structured Outputs (ADK)

This project demonstrates how to use **Structured Outputs** with Google ADK and Gemini to make LLM responses predictable, machine-readable, and schema-enforced for seamless integration into application code.

---

## What are Structured Outputs?

An LLM normally returns free-form text:

```text
Harsh is a BCA student who knows Python and JavaScript...
```

That is useful for humans, but application code usually needs predictable fields.

With Structured Outputs, we define a schema and enforce the model to return data that strictly follows that schema:

```json
{
  "name": "Harsh Chauhan",
  "course": "BCA",
  "skills": ["Python", "JavaScript", "Node.js", "PostgreSQL"],
  "projects": ["DevHub", "Authentication Service"],
  "current_learning": ["Agentic AI", "cybersecurity"]
}
```

### Flow Diagram

```text
Natural Language
       ↓
      LLM
       ↓
    Schema
       ↓
Structured Output
       ↓
Application Code
```

Google's Gemini API supports Structured Outputs using JSON Schema, and the Google GenAI SDK / ADK supports defining schemas effortlessly with **Pydantic** in Python. Structured Outputs are fundamental for data extraction, classification, and reliable multi-agent workflows.

> [!IMPORTANT]
> **Structured Outputs control the shape and type of the response.** They do not automatically guarantee that every value is factually correct. Application-level validation and prompt instruction constraints remain crucial.

---

## Project Goals

This project focuses on:

* Understanding Structured Outputs vs JSON Mode vs Function Calling
* Defining schemas with Pydantic (`BaseModel` and `Field`)
* Using `output_schema` with Google ADK `Agent`
* Extracting structured data from natural language
* Generating predictable structured objects (e.g., Email objects)
* Handling missing information without inventing false details (preventing hallucinations)
* Understanding output formatting vs business-logic validation

---

## Project Structure

```text
04_structured_outputs/
│
├── student_profile/
│   ├── __init__.py
│   └── agent.py
│
├── email_agent/
│   ├── __init__.py
│   └── agent.py
│
└── README.md
```

---

## 1. Student Profile Agent

The Student Profile Agent extracts structured information from a natural-language description.

### Input

```text
My name is Harsh Chauhan. I am pursuing BCA.
I know Python, JavaScript, Node.js and PostgreSQL.
I have built DevHub and an Authentication Service.
Currently I am learning Agentic AI and cybersecurity.
```

### Output

```json
{
  "name": "Harsh Chauhan",
  "course": "BCA",
  "skills": ["Python", "JavaScript", "Node.js", "PostgreSQL"],
  "projects": ["DevHub", "Authentication Service"],
  "current_learning": ["Agentic AI", "cybersecurity"]
}
```

### Schema

A Pydantic model defines the expected structure:

```python
from pydantic import BaseModel, Field


class StudentProfile(BaseModel):
    name: str = Field(description="Student's full name")
    course: str = Field(description="Student's course or degree")
    skills: list[str] = Field(
        description="Technical skills of the student"
    )
    projects: list[str] = Field(
        description="Projects created by the student"
    )
    current_learning: list[str] = Field(
        description="Technologies or subjects the student is currently learning"
    )
```

The ADK configuration is:

```python
root_agent = Agent(
    model="gemini-2.5-flash",
    name="student_profile_agent",
    description="Extracts student profile details.",
    instruction="...",
    output_schema=StudentProfile,
)
```

This ensures the agent's output adheres strictly to the `StudentProfile` Pydantic model.

---

## 2. Email Agent

The Email Agent converts a natural-language request into a structured email object with metadata flags indicating whether critical details were provided.

### Input

```text
Create a professional email to the marketing department requesting
a 45-minute meeting on September 10th at 3:00 PM in Conference Room A
to discuss the new product launch strategy.
```

### Output

```json
{
  "subject": "Meeting Request: New Product Launch Strategy",
  "body": "Dear Marketing Team,\n\nI would like to schedule a meeting...",
  "date_provided": true,
  "time_provided": true,
  "duration_provided": true
}
```

### Schema

```python
from pydantic import BaseModel, Field


class EmailContent(BaseModel):
    subject: str = Field(
        description="Concise and descriptive subject line"
    )
    body: str = Field(
        description="Well-formatted main content of the email"
    )
    date_provided: bool = Field(
        description="Whether the user provided a meeting date"
    )
    time_provided: bool = Field(
        description="Whether the user provided a meeting time"
    )
    duration_provided: bool = Field(
        description="Whether the user provided meeting duration"
    )
```

---

## Handling Missing Information

Handling missing information gracefully is a key capability demonstrated by the Email Agent.

### User Input with Missing Details

```text
Create an email to schedule a meeting with the marketing department
to discuss the new product launch strategy.
```

The user did not provide:
* Date
* Time
* Duration

The agent should **not invent these values**.

### Structured Output Response

```json
{
  "subject": "Meeting Request: New Product Launch Strategy Discussion",
  "body": "Dear Marketing Team,\n\nI would like to schedule a meeting to discuss our strategy for the new product launch. Please let me know your availability so we can coordinate and finalize the meeting details.\n\nBest regards,\n[Your Name]",
  "date_provided": false,
  "time_provided": false,
  "duration_provided": false
}
```

> [!NOTE]
> **Key Principle:**
> 
> ```text
> Structured Output ≠ Guaranteed Factual Correctness
> ```
> 
> The schema controls the **shape** of the result. Instructions and application validation are required to control the **meaning and correctness** of values.

---

## Why Prompt Instructions Still Matter

A schema alone does not inform the model how to react when information is missing. Prompt instructions provide behavioral constraints:

```python
instruction = """
You are a professional email writing assistant.

Create an email based only on the information provided by the user.

Rules:
1. Never invent dates, times, meeting durations, names, locations, or links.
2. If the user does not provide a date or time, do not create one.
3. If important information is missing, set corresponding flags to false.
4. Return only fields defined by the schema.
"""
```

Reliability comes from combining all three layers:

```text
Prompt Instructions  +  Structured Schema  +  Application Validation
```

---

## Structured Outputs vs Normal LLM Output

### Normal Text Output

```text
The meeting could be next Tuesday at 2 PM...
```

* The application code must parse raw unstructured text using regex or heuristics.

### Structured Output

```json
{
  "subject": "...",
  "body": "...",
  "date_provided": false,
  "time_provided": false
}
```

* The application code can directly access object attributes:

```python
email.subject
email.body
email.date_provided
```

This makes LLM output directly compatible with APIs, databases, UI components, and downstream agents.

---

## Structured Outputs vs JSON Mode

| Aspect | JSON Mode | Structured Outputs |
| :--- | :--- | :--- |
| **Enforcement** | Instructs model to output syntax-valid JSON | Constrains decoding to a **specific JSON Schema** |
| **Guarantee** | Valid JSON syntax (keys can vary) | Valid JSON syntax **AND** exact key/type schema contract |
| **Reliability** | Medium (keys might be missing or extra) | High (strictly matching Pydantic / Schema definition) |

```text
JSON Mode:
  LLM ──► Valid JSON syntax

Structured Outputs:
  LLM ──► Defined JSON Schema ──► Predictable structured object
```

---

## Structured Outputs vs Function Calling

These two core capabilities serve distinct purposes:

| Feature | Primary Purpose | Standard Mechanism |
| :--- | :--- | :--- |
| **Structured Outputs** | Format the model's **final response** | `output_schema` parameter |
| **Function Calling** | Allow model to request **tool actions** | `tools=[...]` parameter |
| **Pydantic** | Define and validate data structures | Python models (`BaseModel`) |
| **Prompt Instructions** | Guide model reasoning and constraints | `instruction="..."` prompt |
| **Application Validation** | Enforce domain/business logic | Code-level assertion / validation |

### Conceptual Comparison

```text
Structured Output Flow:
  User ──► LLM ──► EmailContent (Final Response)

Function Calling Flow:
  User ──► LLM ──► send_email(...) ──► External Email System
```

A production agent frequently uses **both** together.

---

## Environment Setup

This example uses the virtual environment created in the root repository.

### Activate Virtual Environment

**Windows PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install google-adk pydantic
```

---

## Environment Variables

Create a `.env` file in your agent folder or root folder:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Ensure `.env` is listed in your `.gitignore` to avoid pushing sensitive credentials.

---

## Running the Agents

From the parent `04_structured_outputs` directory:

### Run Student Profile Agent
```powershell
adk run student_profile
```

### Run Email Agent
```powershell
adk run email_agent
```

### Launch ADK Web Interface
```powershell
adk web
```

---

## Test Prompts

### 1. Student Profile

```text
My name is Harsh Chauhan. I am pursuing BCA.
I know Python, JavaScript, Node.js and PostgreSQL.
I have built DevHub and an Authentication Service.
Currently I am learning Agentic AI and cybersecurity.
```

### 2. Email — Missing Information

```text
Create an email to schedule a meeting with the marketing department
to discuss the new product launch strategy.
```

**Expected Schema Result:**
```json
{
  "date_provided": false,
  "time_provided": false,
  "duration_provided": false
}
```

### 3. Email — Complete Information

```text
Create a professional email to the marketing department requesting
a 45-minute meeting on September 10th at 3:00 PM in Conference Room A
to discuss the new product launch strategy.
```

**Expected Schema Result:**
```json
{
  "date_provided": true,
  "time_provided": true,
  "duration_provided": true
}
```

### 4. Email — Partial Information (Date Only)

```text
Create an email to the marketing department requesting a meeting
on September 10th to discuss the new product launch strategy.
```

* The agent should extract `date_provided = true` while keeping `time_provided = false` without hallucinating a random time.

---

## Important Lessons

1. **LLM output is not automatically reliable:** A model can produce structurally valid JSON with incorrect values.
2. **Schema defines a contract:** It guarantees structural types (e.g., list vs string vs boolean).
3. **Structure ≠ Correctness:** Always pair schemas with prompt constraints and post-processing validation.
4. **Missing information should be handled explicitly:** Design fields (like boolean flags or optional fields) to capture missing context rather than letting the model guess.
5. **Structured outputs power multi-agent workflows:** When output from Agent A becomes input to Agent B, structured schemas eliminate parsing errors.

---

## Key Concepts Covered

```text
Structured Outputs
│
├── JSON Schema
├── Pydantic (BaseModel, Field)
├── Type Validation (Lists, Booleans, Strings)
├── ADK output_schema
├── Hallucination Prevention
├── Missing Information Handling
├── Schema vs Prompt vs Validation
└── Downstream Agent Integration
```

---

## Official Documentation

* [Google Gemini — Structured Outputs](https://ai.google.dev/gemini-api/docs/structured-output)
* [Google Gemini — Structured Outputs with Generate Content](https://ai.google.dev/gemini-api/docs/generate-content/structured-output)
* [Google Agent Development Kit (ADK) Docs](https://google.github.io/adk-docs/)
* [Pydantic Documentation](https://docs.pydantic.dev/)
* [Pydantic Models](https://docs.pydantic.dev/latest/concepts/models/)

---

## Summary

Structured Outputs solve a core challenge in LLM applications: **How to reliably ingest LLM outputs into software systems.**

```text
Student Profile Request  ──►  Pydantic Schema  ──►  Structured JSON
Email Request            ──►  Pydantic Schema  ──►  Structured Email Object
```

* **Structured Outputs** ──► Reliable **FORMAT**
* **Prompts + Validation** ──► Reliable **BEHAVIOR and CORRECTNESS**

---

## Author

**Harsh Chauhan**

* Learning Journey: **Agentic AI with Google ADK**
* Module: **04 — Structured Outputs**
* Started: **2026**

> Learning by building, experimenting, and understanding Agentic AI from the ground up.

---

**Part of the [ADK from Zero](../README.md) learning journey.**
