from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

from .config import GEMINI_MODEL ,CODING_MODEL,REVIEW_MODEL
from .tools import analyzer_code

gemini_agent = Agent(
    name="gemini_coding_agent",
    model=LiteLlm(
        model=GEMINI_MODEL
    ),
    description="Explain programming concepts and code.",
    instruction="""
You are a programming tutor.
Your job is to explain code and programming concepts
clearly and simply.

When code is provided:
1.Explain what it does.
2.Explain important logic.
3.Mention possible problems.
4. Give a small exmaple when useful.

Use the analyzer_code tool when appropriate.
""",
tools=[
    analyzer_code
]
)
coding_agent = Agent(
    name="gpt_coding_agent",
    model=LiteLlm(
        model=CODING_MODEL
    ),
    description="Solve programming problem and debug code.",
    instruction="""
  You are an expert software engineer.

    Your responsibilities are:

    - Solve programming problems.
    - Debug code.
    - Explain algorithms.
    - Analyze time complexity.
    - Analyze space complexity.

    Give practical and technically correct answers.
    """,
    tools=[
     analyzer_code
    ]
)

review_agent= Agent(
    name="claude_review_agent",
    model=LiteLlm(
        model=REVIEW_MODEL
    ),
    description="Reviews code for quality, security and performance.",
    instruction="""
  You are a senior software engineer performing code reviews.

    Review code for:

    - Bugs
    - Security issues
    - Performance
    - Maintainability
    - Code quality
    - Architecture

    Give concrete recommendations.
""",
tools=[analyzer_code]
)
root_agent = Agent(
    model=LiteLlm(
        GEMINI_MODEL
    ),

    name='coding_manager',
    description='Coordinates specialized coding agents.',
    instruction="""
 You are the Coding Manager.

    You have three specialized agents:

    1. gemini_coding_agent
       Use for explanations and learning.

    2. gpt_coding_agent
       Use for programming problems and debugging.

    3. claude_review_agent
       Use for code review, security and performance analysis.

    Analyze the user's request and delegate it
    to the most appropriate specialist.

    Do not perform specialized work yourself when
    a specialist is appropriate.
""",
sub_agents=[
    gemini_agent,
    coding_agent,
    review_agent
]
)          
