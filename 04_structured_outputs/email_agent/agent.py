from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel,Field

class EmailContent(BaseModel):
    subject:str = Field(description="The subject line of the email .Should be concise and descriptive.")
    body:str = Field(description="The main content of the email .Should be well-formatted with proper greeting ,paragraphs, and signature.")
    data_provided:bool=Field(
        description="Wheater the user provided a meeting data."
    )
    time_provided:bool =Field(
        description="Whether the user provided a meeting time"
    )
    duration_provided:bool = Field(
        description="Whether the user provided meeting duration"
    )


root_agent = Agent(
    model='gemini-3.5-flash',
    name='email_agent',
    description='Generates professional emails with structured subject and body.',
    instruction="""
   You are an Email Generation Assistant.
        Your task is to generate a professional email based on the user's request.

        GUIDELINES:
        - Create an appropriate subject line (concise and relevant)
        - Write a well-structured email body with:
            * Professional greeting
            * Clear and concise main content
            * Appropriate closing
            * Your name as signature
        - Suggest relevant attachments if applicable (empty list if none needed)
        - Email tone should match the purpose (formal for business, friendly for colleagues)
        - Keep emails concise but complete

        IMPORTANT: Your response MUST be valid JSON matching this structure:
        {
            "subject": "Subject line here",
            "body": "Email body here with proper paragraphs and formatting",
        }

        DO NOT include any explanations or additional text outside the JSON response.

        You are a professional email writing assistant.

Create an email based only on the information provided by the user.

Important rules:
1. Never invent dates, times, meeting duration, names, locations,
   links, or other specific details.
2. If the user does not provide a date or time, do not create one.
3. If important information is missing, mention that it needs to
   be provided.
4. Return only the subject and body according to the output schema.
""",
output_schema=EmailContent,
output_key="email",
)
