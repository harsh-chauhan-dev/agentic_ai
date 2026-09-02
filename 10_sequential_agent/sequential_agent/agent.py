from google.adk.agents import SequentialAgent

from .sub_agent import (
    research_agent,
    teacher_agent,
    quiz_agent,
    finalizer_agent,
)


root_agent = SequentialAgent(
    name="StudyGuidePipeline",
    description=(
        "A sequential pipeline that transforms a technical topic "
        "into a structured study guide."
    ),
    sub_agents=[
        research_agent,
        teacher_agent,
        quiz_agent,
        finalizer_agent,
    ],
)