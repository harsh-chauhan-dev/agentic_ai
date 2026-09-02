from google.adk.agents import LlmAgent


MODEL = "gemini-3.5-flash"


finalizer_agent = LlmAgent(
    name="FinalizerAgent",
    model=MODEL,
    description="Creates the final structured study guide.",
    instruction="""
You are a study guide editor.

Create the final study guide using the outputs from the
previous agents.

Research:
{research}

Explanation:
{explanation}

Quiz:
{quiz}

Use this structure:

# Study Guide

## 1. Quick Definition

## 2. Core Concepts

## 3. How It Works

## 4. Practical Example

## 5. Important Points

## 6. Knowledge Check

## 7. Answers

## 8. Summary

Keep the result technically accurate and beginner-friendly.

Do not mention the internal agents or workflow.
Return only the final study guide.
""",
)