from google.adk.agents import Agent
from google.adk.tools import google_search

market_analyser = Agent(
    name="market_analyser",
    model="gemini-2.0-flash-exp",
    description="Agent to gather market information for a given project idea using Google Search.",
    instruction="I can search the internet to gather market information for your project idea. Just provide your project idea!",
    tools=[google_search],
) 