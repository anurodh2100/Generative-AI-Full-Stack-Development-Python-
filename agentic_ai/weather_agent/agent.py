# ---------------------------------------------------------
# Weather Agent
# Tool Calling + Planning + In-Memory Conversation + Rich
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
# Load Environment Variables
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

Before using a tool, make a concise internal plan.
Do NOT reveal private chain-of-thought.

Available tools:

1. get_weather
   Get current weather conditions of a city.

2. get_forecast
   Get the weather forecast for a city.

3. get_temperature
   Get the current temperature of a city.

Rules:
- Use the appropriate tool whenever weather information
  is required.
- Do not make up weather information.
- After receiving tool results, provide a concise answer.
- For non-weather questions, politely say that you only
  handle weather-related questions.
"""


# ---------------------------------------------------------
# Weather Tool 1
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
        "error": "Unable to fetch weather."
    }


# ---------------------------------------------------------
# Weather Tool 2
# ---------------------------------------------------------

def get_forecast(city: str):

    url = f"https://wttr.in/{city.lower()}?format=j1"

    response = requests.get(url)

    if response.status_code != 200:
        return {
            "error": "Unable to fetch forecast."
        }

    data = response.json()

    forecast = []

    for day in data["weather"][:3]:

        forecast.append({
            "date": day["date"],
            "max_temperature": day["maxtempC"],
            "min_temperature": day["mintempC"],
            "description": day["hourly"][4]["weatherDesc"][0]["value"]
        })

    return {
        "city": city,
        "forecast": forecast
    }


# ---------------------------------------------------------
# Weather Tool 3
# ---------------------------------------------------------

def get_temperature(city: str):

    url = f"https://wttr.in/{city.lower()}?format=%t"

    response = requests.get(url)

    if response.status_code == 200:
        return {
            "city": city,
            "temperature": response.text.strip()
        }

    return {
        "error": "Unable to fetch temperature."
    }


# ---------------------------------------------------------
# Available Tools
# ---------------------------------------------------------

available_tools = {
    "get_weather": get_weather,
    "get_forecast": get_forecast,
    "get_temperature": get_temperature
}


# ---------------------------------------------------------
# Tool Schemas
# ---------------------------------------------------------

tools = [

    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather conditions of a city.",
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
    },

    {
        "type": "function",
        "function": {
            "name": "get_forecast",
            "description": "Get the weather forecast for a city.",
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
    },

    {
        "type": "function",
        "function": {
            "name": "get_temperature",
            "description": "Get the current temperature of a city.",
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

]


# ---------------------------------------------------------
# In-Memory Conversation
# ---------------------------------------------------------

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
        "Ask me about current weather or forecast.\n"
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


    # -----------------------------------------------------
    # Exit
    # -----------------------------------------------------

    if user_prompt.strip().lower() == "exit":

        console.print(
            "\n[bold green]🤖 Assistant:[/bold green] "
            "Goodbye! 👋"
        )

        break


    # -----------------------------------------------------
    # Add User Message
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


        # -------------------------------------------------
        # Groq Call
        # -------------------------------------------------

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )


        response_time = time.perf_counter() - start_time

        assistant_message = response.choices[0].message


        # -------------------------------------------------
        # Tool Calling
        # -------------------------------------------------

        if assistant_message.tool_calls:

            console.print(
                "\n[bold yellow]🧠 Planning...[/bold yellow]"
            )

            console.print(
                "[bold magenta]🔧 Tool required![/bold magenta]"
            )


            # -------------------------------------------------
            # Add Assistant Tool Call
            # -------------------------------------------------

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


                console.print(
                    f"[bold cyan]🔧 Calling:[/bold cyan] "
                    f"{tool_name}"
                )


                # ---------------------------------------------
                # Get Function From Available Tools
                # ---------------------------------------------

                tool_function = available_tools.get(tool_name)


                if tool_function:

                    tool_result = tool_function(**arguments)

                else:

                    tool_result = {
                        "error": f"Tool '{tool_name}' not found."
                    }


                console.print(
                    "[bold green]✅ Tool executed![/bold green]"
                )


                # ---------------------------------------------
                # Send Tool Result Back To Groq
                # ---------------------------------------------

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
            f"\n[dim]Response Time: "
            f"{response_time:.2f}s[/dim]"
        )


        break