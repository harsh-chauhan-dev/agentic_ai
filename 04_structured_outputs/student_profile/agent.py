from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel,Field


class StudentProfile(BaseModel):
    name:str = Field(description="Student's full name")
    course:str = Field(description="Student's degree or course")
    skills: list[str] = Field(description="Technical skills of the student")
    project:list[str]  = Field(description="Project built by the student")
    current_learning:list[str] = Field(
        description="Technologies or topic the student is currently learning"
    )


root_agent = Agent(
    model='gemini-3.5-flash',
    name='student_profile_agent',
    description='A helpful assistant for user questions.',
    instruction="""
You are a student profile extraction agent.

Extract information form the user's text and return it according to the StudentProfile schema.

Rules:
  - Extract only information present in the input
  - Do not invent skills or project.
  - If information is missing, use an empty list where appropriate.
""",
 output_schema=StudentProfile,
)
