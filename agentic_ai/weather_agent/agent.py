# ---------------------------------------------------------
# Weather Agent
# Tool Calling + Planning + Memory + Rich
# ---------------------------------------------------------

from groq import Groq
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
import requests
import os
import json
import time


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

console = Console()


# ---------------------------------------------------------
# System Prompt
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are an expert Weather Assistant.

Your job is to answer weather-related questions.

Before using a tool, make a concise plan internally.
Do NOT reveal private chain-of-thought.

You have access to this tool:

get_weather(city)

Use the weather tool whenever the user asks for current
weather information.

After receiving the tool result, provide a concise and
natural final answer.

For non-weather questions, politely say that you can only
help with weather-related questions.
"""


# ---------------------------------------------------------
# Weather Tool
# ---------------------------------------------------------

def get_weather(city: str):

    url = f"https://wttr.in/{city.lower()}?format=%C+%t"

    response = requests.get(url)

    if response.status_code == 200:
        return {
            "city": city,
            "weather": response.text.strip()
        }

    return {
        "city": city,
        "error": "Something went wrong while fetching weather."
    }


# ---------------------------------------------------------
# Tool Schema
# ---------------------------------------------------------

weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather of a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Name of the city"
                }
            },
            "required": ["city"]
        }
    }
}


# ---------------------------------------------------------
# Memory
# ---------------------------------------------------------

MEMORY_FILE = "weather_memory.json"

try:
    with open(MEMORY_FILE, "r") as f:
        messages = json.load(f)

except FileNotFoundError:

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]


# ---------------------------------------------------------
# UI
# ---------------------------------------------------------

console.print(
    Panel(
        "[bold]Weather Agent[/bold]\n"
        "Ask me about current weather.\n"
        "Type [yellow]exit[/yellow] to quit.",
        title="🌤️ Assistant"
    )
)


# ---------------------------------------------------------
# Continuous Agent
# ---------------------------------------------------------

while True:

    user_prompt = console.input(
        "\n[bold cyan]👤 You:[/bold cyan] "
    )

    if user_prompt.strip().lower() == "exit":

        console.print(
            "[bold green]🤖 Assistant:[/bold green] "
            "Goodbye! 👋"
        )

        break


    # -----------------------------------------------------
    # Add user message
    # -----------------------------------------------------

    messages.append({
        "role": "user",
        "content": user_prompt
    })


    # -----------------------------------------------------
    # Agent Loop
    # -----------------------------------------------------

    while True:

        start_time = time.perf_counter()

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=[weather_tool],
            tool_choice="auto"
        )

        response_time = time.perf_counter() - start_time

        assistant_message = response.choices[0].message


        # -------------------------------------------------
        # Check Tool Call
        # -------------------------------------------------

        if assistant_message.tool_calls:

            console.print(
                "\n[bold yellow]🧠 Planning...[/bold yellow]"
            )

            console.print(
                "[bold magenta]🔧 Calling weather tool...[/bold magenta]"
            )


            # Add assistant tool-call message
            messages.append({
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    }
                    for tool_call in assistant_message.tool_calls
                ]
            })


            # -------------------------------------------------
            # Execute Tools
            # -------------------------------------------------

            for tool_call in assistant_message.tool_calls:

                tool_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )


                if tool_name == "get_weather":

                    city = arguments["city"]

                    console.print(
                        f"[bold cyan]📍 City:[/bold cyan] {city}"
                    )

                    tool_result = get_weather(city)


                    console.print(
                        "[bold green]🌤️ Weather data received![/bold green]"
                    )


                    # -----------------------------------------
                    # Send Tool Result Back to Groq
                    # -----------------------------------------

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result)
                    })


            # ---------------------------------------------
            # Continue Agent Loop
            # ---------------------------------------------

            continue


        # -------------------------------------------------
        # Final Answer
        # -------------------------------------------------

        final_answer = assistant_message.content

        messages.append({
            "role": "assistant",
            "content": final_answer
        })

        console.print(
            "\n[bold green]🤖 Assistant:[/bold green]"
        )

        console.print(final_answer)

        console.print(
            f"\n[dim]Response Time: {response_time:.2f}s[/dim]"
        )

        break


    # -----------------------------------------------------
    # Save Memory
    # -----------------------------------------------------

    with open(MEMORY_FILE, "w") as f:

        json.dump(
            messages,
            f,
            indent=4
        )