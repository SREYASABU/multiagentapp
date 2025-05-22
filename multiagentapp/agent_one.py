
from google.adk.agents import Agent

from .agents.subagents.market_analyser.market_analyser import market_analyser
from .agents.subagents.competitor_identifier.competitor_identifier import competitor_identifier
import os

from google.adk.models.lite_llm import LiteLlm




# AGENT_MODEL = "ollama/qwen3:4b"
AGENT_MODEL = "gemini/gemini-2.0-flash"
# AGENT_MODEL = "gemini/gemini-2.5-flash-preview-05-20"


root_agent = Agent(
    name="root_coordinator_agent",
    model="gemini-2.0-flash",
    description="A coordinator agent that handles user queries by first gathering market information and then identifying competitors.",
    instruction=(
        "You are the main coordinator. Your role is to first delegate the user's project idea "
        "to the market_analyser to gather market information. "
        "Once you receive the search results from the market_analyser, "
        "you must then pass these results to the competitor_identifier to extract and list competitors. "
        "Do not answer the user query yourself directly. Always use the market_analyser first, then the competitor_identifier."
    ),
    sub_agents=[market_analyser, competitor_identifier], 
    tools=[],
)

