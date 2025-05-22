# agent_runner.py
import os
import asyncio
from dotenv import load_dotenv # Don't forget this!
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Make sure this import matches your project structure
# It now imports the root_agent from the 'agents' package
from .agent_one import root_agent



session_service = InMemorySessionService()


def get_or_create_session(
    app_name: str, user_id: str, session_id: str, initial_state: dict
):
    retrieved_session = session_service.get_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )
    if retrieved_session:
        return retrieved_session
    return session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id, state=initial_state
    )


def get_runner(app_name, agent):
    runner = Runner(
        agent=agent,  # The agent we want to run (which is our root_agent)
        app_name=app_name,  # Associates runs with our app
        session_service=session_service,  # Uses our session manager
    )
    return runner


async def call_agent_async(query: str, runner: Runner, user_id: str, session_id: str):
    """Sends a query to the agent and prints the final response."""
    print(f"\n>>> User Query: {query}")

    content = types.Content(role="user", parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response."  # Default

    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        # Print detailed event information for debugging the multi-agent flow
        event_content_preview = ""
        if event.content and event.content.parts:
            event_content_preview = event.content.parts[0].text[:100] + "..." if event.content.parts[0].text else ""
        elif event.tool_code and event.tool_code.name:
            event_content_preview = f"Tool: {event.tool_code.name}"
        elif event.actions and event.actions.escalate:
            event_content_preview = "Escalated"
        else:
            event_content_preview = str(event.content) # Fallback for other content types

        print(
            f"  [Event] Author: {event.author}, Type: {type(event).__name__}, "
            f"Final: {event.is_final_response()}, Content Preview: '{event_content_preview}'"
        )
        if event.tool_code:
            print(f"       Tool Call: {event.tool_code.name}, Args: {event.tool_code.args}")
        if event.tool_response:
            print(f"       Tool Response: {event.tool_response.tool_output_parts[0].text[:100]}") # Only show first 100 chars


        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = (
                    f"Agent escalated: {event.error_message or 'No specific message.'}"
                )
            break  # Stop processing events once the final response is found

    print(f"<<< Agent Response: {final_response_text}")
    return final_response_text


async def main():
    # Define constants for identifying the interaction context
    APP_NAME = "multi_agent_search_answer_app" # Give it a descriptive app name
    USER_ID = "multi_user_1"
    SESSION_ID = "multi_session_001"  # Using a fixed ID for simplicity

    """
    No prefix: Session-specific, persists only for the current session
    user:: User-specific, persists across all sessions for a particular user
    app:: Application-wide, shared across all users and sessions
    temp:: Temporary, exists only during the current execution cycle
    """
    initial_state = {"user:preferences": {"language": "English"}}
    get_or_create_session(APP_NAME, USER_ID, SESSION_ID, initial_state)
    
    # Use the root_agent from our agents package
    runner = get_runner(APP_NAME, root_agent)
    print(f"Runner created for agent '{runner.agent.name}'.")

    while True:
        text = input("Enter your query (or 'exit' to quit): ")
        if text.lower() == "exit":
            break
        await call_agent_async(
            text, runner=runner, user_id=USER_ID, session_id=SESSION_ID
        )


if __name__ == "__main__":
    asyncio.run(main())