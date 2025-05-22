from google.adk.agents import LlmAgent
import os
from dotenv import load_dotenv

load_dotenv()

competitor_identifier = LlmAgent(
    name="competitor_identifier",
    model="gemini-2.0-flash-exp",
    description="An agent that extracts and lists competitors from search results for a given project idea.",
    instruction=(
        "You are a competitor identification specialist. Your task is to analyze the provided search results "
        "and extract a list of competitors implementing the given project idea. "
        "Focus on company names and brief descriptions. "
        "Do not perform any searches yourself. Rely solely on the information given to you. "
        "If the information is insufficient, state that clearly."
        "Start your answer directly without preamble."
    ),
    tools=[],  # This agent does not need any tools, it only processes text
) 