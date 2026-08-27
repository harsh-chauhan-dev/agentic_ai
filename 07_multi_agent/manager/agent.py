from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from sub_agents.funny_nerd.agent import funny_nerd
from sub_agents.stock_analyst.agent import stock_analyst
from sub_agents.news_analyst.agent import news_analyst
from tools.tools import get_current_time
root_agent = Agent(
    name="root_agent",
    model="gemini-3.5-flash",
    description="A manager agent that delegates tasks to specialized agents.",
    instruction="""
    You are the manager agent.

    Delegate tasks to the appropriate specialized agent:

    - Stock prices and stock market data -> stock_analyst
    - News and current news -> news_analyst
    - Nerdy jokes -> funny_nerd

    Do not answer real-time stock or news questions yourself.
    Delegate those requests to the appropriate agent.
    """,
    sub_agents=[stock_analyst, funny_nerd],
    tools=[
        AgentTool(news_analyst),
        get_current_time,
    ],
)