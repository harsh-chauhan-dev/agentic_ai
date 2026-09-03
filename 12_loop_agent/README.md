# 12 --- Loop Agent: LinkedIn Post Generation & Refinement

A multi-agent LinkedIn post generation system built with **Google Agent
Development Kit (ADK)**.

This is the **final project in this Agentic AI project series**. It
demonstrates how a `LoopAgent` can repeatedly review and refine an
LLM-generated result until the defined quality requirements are
satisfied.

------------------------------------------------------------------------

## 📌 Project Introduction

Creating a good technical LinkedIn post is not only about generating
text once.

A useful workflow is:

``` text
Generate
   ↓
Review
   ↓
Identify Problems
   ↓
Refine
   ↓
Review Again
   ↓
Pass Requirements?
   ├── No → Refine again
   └── Yes → Exit loop
```

This project implements that workflow using ADK's **`LoopAgent`**.

The system first generates a LinkedIn post, then enters a refinement
loop where a reviewer checks the post and a refiner improves it based on
the review feedback.

------------------------------------------------------------------------

## 🎯 Project Goal

The goal is to demonstrate the core principle of a **Loop Agent**:

> **Iteratively execute a group of agents until the desired result is
> achieved or the maximum number of iterations is reached.**

The project focuses on a practical use case: generating and improving a
technical LinkedIn post about learning **Google Agent Development Kit
(ADK)**.

------------------------------------------------------------------------

## 🧠 How the Loop Agent Works

The application contains two major stages.

### 1. Initial Post Generation

The `InitialPostGenerator` creates the first version of the LinkedIn
post.

It is instructed to include:

1.  A strong opening hook
2.  What was built
3.  Technical concepts used
4.  The problem being solved
5.  What was learned
6.  A simple closing / CTA

The generated post is stored in the shared state as:

``` text
current_post
```

The generator is defined as an `LlmAgent` and writes its output to
`current_post`.

------------------------------------------------------------------------

### 2. Post Refinement Loop

After the initial post is generated, the `PostRefinementLoop` starts.

The loop contains two agents:

``` text
PostReviewer
     ↓
PostRefinerAgent
```

The loop is configured with a maximum of **2 iterations**.

``` python
refinement_loop = LoopAgent(
    name="PostRefinementLoop",
    max_iterations=2,
    sub_agents=[
        post_reviewer,
        post_refiner,
    ],
)
```

------------------------------------------------------------------------

## 🔍 Post Reviewer

The `PostReviewer` evaluates the current LinkedIn post.

It first uses the `count_characters` tool to verify that the post is
between:

``` text
Minimum: 1000 characters
Maximum: 1500 characters
```

It then checks requirements such as:

-   `@aiwithbrandon` is mentioned
-   At least 4 ADK capabilities are included
-   A clear call-to-action exists
-   Practical applications are included
-   Genuine enthusiasm is shown
-   No emojis
-   No hashtags
-   Professional tone
-   Conversational style
-   Clear and concise writing

The reviewer stores its feedback in:

``` text
review_feedback
```

The reviewer uses both `count_characters` and `exit_loop` as tools.
fileciteturn2file2L20-L34 fileciteturn2file2L44-L58

------------------------------------------------------------------------

## ✍️ Post Refiner

If the reviewer identifies problems, `PostRefinerAgent` receives:

``` text
Current Post
+
Review Feedback
```

It then improves the existing post while maintaining its original tone
and theme.

The refiner is specifically instructed to maintain the required content
and style, including the 1000--1500 character range, no emojis, and no
hashtags. fileciteturn2file1L18-L41

The improved result is written back to:

``` text
current_post
```

This means the next loop iteration reviews the newly improved version.

------------------------------------------------------------------------

## 🛑 Loop Termination

The project uses an `exit_loop` tool to terminate the refinement process
when the reviewer determines that all requirements have been satisfied.

The tool sets:

``` python
tool_context.actions.escalate = True
```

which signals the loop to stop. fileciteturn2file3L62-L79

Therefore, the system has two possible stopping conditions:

``` text
Quality requirements satisfied
          OR
Maximum iterations reached
```

------------------------------------------------------------------------

## 🏗️ Architecture

``` text
                 User Project Information
                          │
                          ▼
              ┌──────────────────────┐
              │ InitialPostGenerator │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  PostRefinementLoop  │
              │     LoopAgent        │
              └──────────┬───────────┘
                         │
                         ▼
                ┌────────────────┐
                │  PostReviewer  │
                └───────┬────────┘
                        │
                 Review Feedback
                        │
                        ▼
                ┌────────────────┐
                │ PostRefinerAgent│
                └───────┬────────┘
                        │
                        ▼
                  Updated Post
                        │
                        └──────────────┐
                                       │
                                  Loop Again
                                       │
                                       ▼
                                  PostReviewer
```

------------------------------------------------------------------------

## 🔗 Agent Structure

The complete application uses a `SequentialAgent` as the root pipeline.

``` text
LinkedInPostGenerationPipeline
│
├── InitialPostGenerator
│
└── PostRefinementLoop
    │
    ├── PostReviewer
    │
    └── PostRefinerAgent
```

The root pipeline first generates the initial post and then passes it
into the refinement loop. fileciteturn2file5L14-L32

------------------------------------------------------------------------

## 🛠️ Tools

### `count_characters`

Checks whether the generated post satisfies the required character
range.

``` text
1000–1500 characters
```

It also stores the review status in session state:

``` text
review_status = "pass"
```

or:

``` text
review_status = "fail"
```

fileciteturn2file3L12-L16 fileciteturn2file3L27-L58

### `exit_loop`

Signals that the post has successfully passed the review requirements
and that the refinement loop should terminate.
fileciteturn2file3L62-L79

------------------------------------------------------------------------

## 📁 Project Structure

``` text
12_loop_agent/
│
├── __init__.py
│
├── agent.py
│
├── tools.py
│
└── subagents/
    │
    ├── post_generator.py
    ├── post_reviewer.py
    └── post_refine.py
```

### File Responsibilities

  -----------------------------------------------------------------------
  File                                Responsibility
  ----------------------------------- -----------------------------------
  `agent.py`                          Defines the root pipeline and
                                      `LoopAgent`

  `post_generator.py`                 Generates the initial LinkedIn post

  `post_reviewer.py`                  Reviews the post and decides
                                      whether refinement is required

  `post_refine.py`                    Improves the post using review
                                      feedback

  `tools.py`                          Provides character validation and
                                      loop termination tools

  `__init__.py`                       Exposes the root agent
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 🔄 Complete Execution Flow

### Step 1 --- User provides project information

Example:

``` text
I built a Parallel Code Review Agent using Google ADK.

It uses ParallelAgent to review code from multiple perspectives:
bugs, security and performance.
```

### Step 2 --- InitialPostGenerator

Creates the first LinkedIn post.

``` text
User Input
   ↓
InitialPostGenerator
   ↓
current_post
```

### Step 3 --- PostReviewer

Reviews the generated post.

``` text
current_post
   ↓
PostReviewer
   ↓
count_characters
   ↓
Quality checks
```

### Step 4 --- PostRefinerAgent

If requirements are not satisfied:

``` text
current_post
+
review_feedback
        ↓
PostRefinerAgent
        ↓
updated current_post
```

### Step 5 --- Loop

The updated post goes through the reviewer again.

``` text
Review
  ↓
Refine
  ↓
Review
  ↓
Refine
  ↓
...
```

### Step 6 --- Exit

When all requirements are satisfied, `exit_loop` signals the loop to
terminate.

------------------------------------------------------------------------

## ⚙️ Installation

Install the required dependencies:

``` bash
pip install google-adk
```

Create your environment file:

``` text
.env
```

Add your Gemini API configuration:

``` env
GOOGLE_API_KEY=your_google_api_key
```

------------------------------------------------------------------------

## ▶️ Run the Project

From the parent directory of the project:

``` bash
adk web
```

Then select:

``` text
12_loop_agent
```

Enter your project information and observe the agent execution.

------------------------------------------------------------------------

## 🧪 Example Input

``` text
I built a Parallel Code Review Agent using Google ADK.

It uses ParallelAgent to review source code from three independent perspectives:
bug and logic analysis, security vulnerability analysis, and performance analysis.

The goal is to make code review faster by running independent reviews in parallel.

While building it, I learned how ParallelAgent executes multiple agents concurrently and how their outputs can be combined into a final review.
```

------------------------------------------------------------------------

## 📚 Key ADK Concepts Demonstrated

### `LlmAgent`

Used to create specialized agents for:

-   LinkedIn post generation
-   Post reviewing
-   Post refinement

### `SequentialAgent`

Used to create the overall pipeline:

``` text
Generator → Refinement Loop
```

### `LoopAgent`

Used to repeatedly execute:

``` text
Reviewer → Refiner
```

until the loop exits or reaches its iteration limit.

### Shared State

The workflow uses state values such as:

``` text
current_post
review_feedback
review_status
```

This allows different agents and tools to work with the evolving result.

### Tool Calling

The reviewer can call:

``` text
count_characters
exit_loop
```

to validate the post and control the workflow.

------------------------------------------------------------------------

## 💡 Core Principle

A normal LLM workflow often looks like:

``` text
Input → LLM → Output
```

A Loop Agent introduces iterative reasoning and refinement:

``` text
Input
  ↓
Generate
  ↓
Evaluate
  ↓
Improve
  ↓
Evaluate
  ↓
Improve
  ↓
Stop
```

This is useful when the first generated result is unlikely to be good
enough and needs repeated evaluation and improvement.

------------------------------------------------------------------------

## ⚠️ Iteration Limit

The refinement loop is configured with:

``` python
max_iterations=2
```

This provides a safety boundary so the workflow does not continue
indefinitely.

The loop can therefore terminate because:

1.  The reviewer calls `exit_loop`, or
2.  The configured maximum number of iterations is reached.

------------------------------------------------------------------------

## 🧩 What This Project Demonstrates

This final project brings together several important agentic workflow
concepts:

``` text
Specialized Agents
       +
Sequential Workflow
       +
Shared State
       +
Tool Calling
       +
Quality Evaluation
       +
Iterative Refinement
       =
Loop-Based Agentic Workflow
```

The important idea is not simply generating a LinkedIn post.

The important idea is building a workflow that can **evaluate its
output, improve it, and repeat the process under controlled
conditions**.

------------------------------------------------------------------------

## 📖 Official Documentation

-   **Google ADK Documentation:** https://google.github.io/adk-docs/
-   **ADK Python Agents:** https://google.github.io/adk-docs/agents/
-   **ADK Workflow Agents:**
    https://google.github.io/adk-docs/agents/workflow-agents/
-   **LoopAgent:**
    https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/

------------------------------------------------------------------------

## 👨‍💻 Author

**Harsh Chauhan**

Software Developer \| Agentic AI Enthusiast

This repository is part of a practical Agentic AI project series built
with **Google Agent Development Kit (ADK)**.

------------------------------------------------------------------------

## ⭐ Final Project

**`12_loop_agent` is the final project of this Agentic AI project
series.**

It concludes the series with an important agentic workflow pattern:

> **Generate → Evaluate → Refine → Repeat**

The project demonstrates how multiple specialized agents can be composed
into a controlled iterative workflow to produce a better final result.
