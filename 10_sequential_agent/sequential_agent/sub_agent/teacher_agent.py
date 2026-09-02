from google.adk.agents import LlmAgent


MODEL = "gemini-3.5-flash"


teacher_agent = LlmAgent(
    name="TeacherAgent",
    model=MODEL,
    description="Explains technical concepts in a beginner-friendly way.",
    instruction="""
You are a technical teacher.

Use the research produced by the previous agent.

Research:
{research}

Explain the topic in a beginner-friendly way.

Include:

- Simple definition
- Core concepts
- Step-by-step explanation
- Important terminology
- Practical example
- Code example when appropriate

Do not create a quiz.
Your output will be passed to the next agent.
""",
    output_key="explanation",
)