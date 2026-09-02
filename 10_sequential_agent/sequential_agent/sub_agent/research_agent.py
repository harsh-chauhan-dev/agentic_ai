from google.adk.agents import LlmAgent


MODEL = "gemini-3.5-flash"


research_agent = LlmAgent(
    name="ResearchAgent",
    model=MODEL,
    description="Researches the key concepts of a technical topic.",
    instruction="""
You are a technical research assistant.

Analyze the topic provided by the user.

Identify:

- Definition
- Core concepts
- Important terminology
- How it works
- Real-world use cases
- Important points for beginners

Keep the research concise and technically accurate.

Do not create the final study guide.
Your output will be passed to another agent.
""",
    output_key="research",
)