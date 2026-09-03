"""
LinkedIn Post Generator Agent

This agent generates the initial LinkedIn post before refinement.
"""

from google.adk.agents.llm_agent import LlmAgent

# Constants
GEMINI_MODEL = "gemini-3.5-flash"

# Define the Initial Post Generator Agent
initial_post_generator = LlmAgent(
    name="InitialPostGenerator",
    model=GEMINI_MODEL,
    instruction="""
You are an expert LinkedIn technical content writer.

Create a LinkedIn post from the project information provided by
the user.

The post should contain:

1. A strong opening hook
2. What was built
3. The technical concepts used
4. What problem it solves
5. What I learned
6. A simple closing/CTA

Rules:
- Sound like a real developer, not a marketing company.
- Keep it concise.
- Use natural LinkedIn formatting.
- Do not invent technologies or features.
- Return ONLY the LinkedIn post.
    """,
    description= "Creates a LinkedIn post from project information.",
    output_key="current_post",
)