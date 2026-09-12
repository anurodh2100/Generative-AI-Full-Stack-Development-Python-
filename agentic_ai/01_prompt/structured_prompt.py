# ---------------------------------------------------------
# Few-Shot Prompting + Continuous Chatbot
# ---------------------------------------------------------
# Few-shot prompting: Give multiple examples to the LLM
# so it learns how to handle different types of inputs.
#
# This bot also:
# - Handles coding/non-coding inputs
# - Returns JSON when code is requested
# - Keeps running until user types "exit"
# ---------------------------------------------------------


from groq import Groq
from dotenv import load_dotenv
import os


# Load API key from .env
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ---------------------------------------------------------
# System Prompt
# ---------------------------------------------------------
# Rules tell the model what to do.
# Examples show the model how to behave.
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are a helpful Coding Assistant.

Rules:

1. Answer coding/programming questions.

2. If the user asks for code, return valid JSON:
{
    "language": "...",
    "explanation": "...",
    "code": "..."
}

3. For non-coding questions, politely refuse.

4. For greetings, greet the user.

5. For unclear input, ask for clarification.


Examples:

User: What is a Python list?
Assistant: A list is an ordered and mutable collection in Python.

User: Write Python code to reverse a string.
Assistant:
{
    "language": "Python",
    "explanation": "A string can be reversed using slicing.",
    "code": "text = 'hello'\\nprint(text[::-1])"
}

User: What is the capital of India?
Assistant: Sorry, I can only help with coding questions.

User: Hi
Assistant: Hello! How can I help you with coding today?

User: asdfghjkl
Assistant: I'm not sure what you mean. Please ask a clear question.

Follow these rules and examples for new inputs.
"""


# ---------------------------------------------------------
# Continuous Chatbot
# ---------------------------------------------------------
# while True keeps the chatbot running.
# It stops only when the user types "exit".
# ---------------------------------------------------------

while True:

    user_prompt = input("\nYou: ")


    # Exit command is handled by Python,
    # so no API call is made for "exit".
    if user_prompt.strip().lower() == "exit":

        print("Assistant: Goodbye! 👋")
        break


    # Send system instructions + user input to the LLM
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


    # Extract and print the model's response
    print(
        "Assistant:",
        response.choices[0].message.content
    )