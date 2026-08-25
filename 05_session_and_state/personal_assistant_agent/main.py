import asyncio
import os
from google.genai import errors

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent


load_dotenv()

APP_NAME = "sessions_and_state"
USER_ID = "harsh"
SESSION_ID = "session_001"


async def main():

    # -----------------------------
    # 1. Create Session Service
    # -----------------------------

    session_service = InMemorySessionService()

    # -----------------------------
    # 2. Create Session
    # -----------------------------

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state={
            "user_name": "Harsh",
            "learning_topic": "Python",
        },
    )

    print("Session created:")
    print(session.id)

    print("\nInitial state:")
    print(session.state)

    # -----------------------------
    # 3. Create Runner
    # -----------------------------

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # -----------------------------
    # 4. Chat Function
    # -----------------------------

    async def ask_agent(message):

        content = types.Content(
            role="user",
            parts=[
                types.Part(text=message)
            ],
        )

        response_text = ""

        try:

            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=SESSION_ID,
                new_message=content,
            ):

                if event.is_final_response():

                    if event.content and event.content.parts:
                        response_text = event.content.parts[0].text

            return response_text

        except errors.ServerError as e:

            if "503" in str(e):
                return "Gemini is temporarily unavailable. Please try again."

            return f"Server error: {e}"

        except Exception as e:

            return f"Error: {e}"
    # -----------------------------
    # 5. Chat Loop
    # -----------------------------

    print("\n===================================")
    print(" Personal Assistant")
    print(" Type 'exit' to quit")
    print("===================================\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("\nGoodbye!")
            break

        response = await ask_agent(user_input)

        print(f"Agent: {response}\n")


if __name__ == "__main__":
    asyncio.run(main())