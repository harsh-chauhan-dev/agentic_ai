from google.adk.agents import Agent

def calculate(a:float,b:float,operation:str) -> float:
    """Perform a basic mathematical calcculation."""

    if operation =="add":
        return a+b

    if operation =="subtract":
        return a-b

    if operation =="multiply":
        return a*b

    if operation =="divide":
        if b==0:
            return 0
        return a/b

    return 0

def get_capital_city(country:str) -> str:
    """Retrun the capital city of a country."""

    capital = {
        "india": "New Delhi",
        "france": "Paris",
        "japan": "Tokyo",
        "germany": "Berlin",
        "usa": "Washington, D.C.",
    }
    return capital.get(
        country.lower(),
        "I don't know the capital of that country."
    )
   
root_agent = Agent(
    model="gemini-3.5-flash",
    name="simple_agent",
    description="An assistant that can perform calculcations.",
    instruction="""
You are a helpful calculcator assistant.

When the uer ask for a calculation,E
use the calculate tool,

Explain the result clearly.""",
tools=[calculate,get_capital_city],
)