from google.adk.agents import Agent
from google.adk.tools import google_search


news_analyst = Agent(
    name="news_analyst",
    model="gemini-3.5-flash",
    description="News analyst agent",
    instruction="""
You are a helpful assistant that can analyze news articales and provide a summary of the news.

when asked about news ,you should use the google_serach tool to search for the news.
If the user ask for news using a relative time , you should use the get_current_time tool to get """,
tools=[google_search],
)