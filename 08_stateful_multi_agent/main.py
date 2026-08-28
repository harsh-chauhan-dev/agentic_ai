import asyncio

from customer_service_agent.agent import customer_service_agent
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from utils import (
    add_user_query_to_history,
    call_agent_async,
)

load_dotenv()

session_service = InMemorySessionService()

initial_state = {
    "user_name": "Harsh Chauhan",
    "purchased_courses": [],
    "interaction_history": [],
}


async def main_async():
    # Setup constants
    APP_NAME = "Customer Support"
    USER_ID = "aiwithbrandon"

    # ===== PART 3: Session Creation =====
    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )

    SESSION_ID = new_session.id
    print(f"Created new session: {SESSION_ID}")

    # ===== PART 4: Agent Runner Setup =====
    runner = Runner(
        agent=customer_service_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # ===== PART 5: Interactive Conversation Loop =====
    print("\nWelcome to Customer Service Chat!")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Goodbye!")
            break

        # Update interaction history with user's query
        await add_user_query_to_history(
            session_service,
            APP_NAME,
            USER_ID,
            SESSION_ID,
            user_input,
        )

        # Process user query
        await call_agent_async(
            runner,
            USER_ID,
            SESSION_ID,
            user_input,
        )

    # ===== PART 6: State Examination =====
    final_session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    print("\nFinal Session State:")

    for key, value in final_session.state.items():
        print(f"{key}: {value}")


def main():
    """Entry point for the application."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()