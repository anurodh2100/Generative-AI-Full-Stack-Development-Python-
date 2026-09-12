# ---------------------------------------------------------
# Few-Shot Prompting + Continuous Chatbot
# ---------------------------------------------------------
# This chatbot demonstrates:
#
# 1. Few-shot prompting
# 2. Handling different types of user inputs
# 3. Continuous conversation using a while loop
# 4. "exit" command to close the chatbot
# ---------------------------------------------------------


from groq import Groq
from dotenv import load_dotenv
import os


# ---------------------------------------------------------
# 1. Load environment variables
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# 2. Create Groq client
# ---------------------------------------------------------

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ---------------------------------------------------------
# 3. System Prompt
# ---------------------------------------------------------
# We provide multiple examples so that the model learns
# how to handle different types of user inputs.
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are a helpful Coding Assistant.

Your job is to answer coding and programming-related
questions.

Follow these examples to understand how to handle
different types of user inputs.

Example 1:

User: What is a Python list?
Assistant: A list is an ordered, mutable collection in Python
that can store multiple values.

Example 2:

User: How do I reverse a string in Python?
Assistant: You can reverse a string using slicing:
text[::-1]

Example 3:

User: What is the capital of India?
Assistant: Sorry, I can only help with coding and programming
related questions.

Example 4:

User: Hi
Assistant: Hello! How can I help you with coding today?

Example 5:

User: asdfghjkl
Assistant: I'm not sure what you mean. Please ask a clear
coding-related question.

Example 6:

User: Tell me a joke.
Assistant: Sorry, I can only help with coding and programming
related questions.

Use the patterns from these examples when handling the
user's input.
"""


# ---------------------------------------------------------
# 4. Continuous Chatbot
# ---------------------------------------------------------
# while True means:
#
# Keep asking for user input continuously.
#
# The loop will only stop when we explicitly use "break".
# ---------------------------------------------------------

while True:

    # -----------------------------------------------------
    # Take input from the user
    # -----------------------------------------------------

    user_prompt = input("\nYou: ")


    # -----------------------------------------------------
    # Check whether user wants to exit
    # -----------------------------------------------------
    # .lower() makes EXIT, Exit, eXiT etc. all work.
    # .strip() removes unnecessary spaces.
    # -----------------------------------------------------

    if user_prompt.strip().lower() == "exit":

        print("Assistant: Goodbye! 👋")

        # Stop the while loop
        break


    # -----------------------------------------------------
    # Send user input to Groq
    # -----------------------------------------------------

    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )


    # -----------------------------------------------------
    # Extract and print the model's response
    # -----------------------------------------------------

    print(
        "Assistant:",
        response.choices[0].message.content
    )