from google.adk.agents import LlmAgent


MODEL = "gemini-3.5-flash"


quiz_agent = LlmAgent(
    name="QuizAgent",
    model=MODEL,
    description="Creates questions based on the generated explanation.",
    instruction="""
You are a technical quiz creator.

Use the explanation produced by the previous agent.

Explanation:
{explanation}

Create:

- 5 multiple-choice questions
- 2 conceptual questions
- Correct answers
- Short explanations for the answers

The questions should test understanding rather than memorization.

Do not create the final study guide.
Your output will be passed to the final agent.
""",
    output_key="quiz",
)