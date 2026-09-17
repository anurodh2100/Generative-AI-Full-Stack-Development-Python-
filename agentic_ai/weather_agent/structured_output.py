import json
import os

import requests
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel


# ============================================================
# SETUP
# ============================================================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

console = Console()

MODEL = "openai/gpt-oss-120b"


# ============================================================
# PYDANTIC OUTPUT FORMAT
# ============================================================

class Forecast(BaseModel):
    date: str
    max_temp: str
    min_temp: str
    description: str


class WeatherData(BaseModel):
    city: str
    temperature: str
    condition: str
    forecast: list[Forecast]


class OutputFormat(BaseModel):
    results: list[WeatherData]


# ============================================================
# WEATHER TOOLS
# ============================================================

def get_weather(city: str):
    """
    Get current weather of a city.
    """

    url = f"https://wttr.in/{city}?format=%C+%t"

    response = requests.get(
        url,
        timeout=10
    )

    if response.status_code != 200:
        return {
            "city": city,
            "error": "Unable to fetch current weather."
        }

    return {
        "city": city,
        "weather": response.text.strip()
    }


def get_forecast(city: str):
    """
    Get 3-day weather forecast of a city.
    """

    url = f"https://wttr.in/{city}?format=j1"

    response = requests.get(
        url,
        timeout=10
    )

    if response.status_code != 200:
        return {
            "city": city,
            "error": "Unable to fetch forecast."
        }

    data = response.json()

    forecast = []

    for day in data["weather"][:3]:

        forecast.append({
            "date": day["date"],
            "max_temp": day["maxtempC"],
            "min_temp": day["mintempC"],
            "description": day["hourly"][4]["weatherDesc"][0]["value"]
        })

    return {
        "city": city,
        "forecast": forecast
    }


def get_temperature(city: str):
    """
    Get current temperature of a city.
    """

    url = f"https://wttr.in/{city}?format=%t"

    response = requests.get(
        url,
        timeout=10
    )

    if response.status_code != 200:
        return {
            "city": city,
            "error": "Unable to fetch temperature."
        }

    return {
        "city": city,
        "temperature": response.text.strip()
    }


# ============================================================
# AVAILABLE TOOLS
# ============================================================

available_tools = {
    "get_weather": get_weather,
    "get_forecast": get_forecast,
    "get_temperature": get_temperature
}


# ============================================================
# TOOL SCHEMAS
# ============================================================

tools = [

    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": (
                "Get the current weather condition and "
                "temperature of a city."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city."
                    }
                },
                "required": ["city"],
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_forecast",
            "description": (
                "Get the 3-day weather forecast "
                "of a city."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city."
                    }
                },
                "required": ["city"],
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_temperature",
            "description": (
                "Get the current temperature "
                "of a city."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city."
                    }
                },
                "required": ["city"],
                "additionalProperties": False
            }
        }
    }
]


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are an intelligent weather agent.

You have access to these tools:

1. get_weather
   - Gets current weather condition and temperature.

2. get_forecast
   - Gets 3-day weather forecast.

3. get_temperature
   - Gets current temperature.

IMPORTANT RULES:

1. If the user asks for BOTH current weather AND forecast,
   ALWAYS call BOTH get_weather and get_forecast.

2. If the user mentions multiple cities,
   process EVERY city.

3. For multiple cities, call the required tools
   separately for each city.

Example:

User:
"Weather and forecast of Indore and Delhi"

You MUST call:

get_weather("Indore")
get_forecast("Indore")
get_weather("Delhi")
get_forecast("Delhi")

4. Never skip a requested city.

5. If user asks only for current weather,
   call get_weather for every requested city.

6. If user asks only for forecast,
   call get_forecast for every requested city.

7. If user asks only for temperature,
   call get_temperature for every requested city.

8. Continue calling tools until all requested
   information has been collected.

9. Do not invent weather information.

10. After all required tool calls are completed,
    provide the final answer.
"""


# ============================================================
# RUN AGENT
# ============================================================

def run_agent(user_query: str):

    messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },

        {
            "role": "user",
            "content": user_query
        }

    ]

    # --------------------------------------------------------
    # AGENT LOOP
    # --------------------------------------------------------

    while True:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        # Save assistant response
        messages.append(assistant_message)

        # ----------------------------------------------------
        # No more tools required
        # ----------------------------------------------------

        if not assistant_message.tool_calls:

            break

        # ----------------------------------------------------
        # Execute ALL tool calls
        # ----------------------------------------------------

        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            console.print(
                f"🔧 Calling: "
                f"[bold]{tool_name}[/bold]"
                f"({arguments})"
            )

            # Get function from registry
            tool_function = available_tools.get(
                tool_name
            )

            if tool_function is None:

                tool_result = {
                    "error": f"Tool '{tool_name}' not found."
                }

            else:

                try:

                    tool_result = tool_function(
                        **arguments
                    )

                    console.print(
                        "✅ Tool executed!"
                    )

                except Exception as e:

                    tool_result = {
                        "error": str(e)
                    }

                    console.print(
                        f"❌ Tool error: {e}"
                    )

            # Send tool result back to LLM
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(tool_result)
                }
            )

    # ========================================================
    # FINAL STRUCTURED OUTPUT
    # ========================================================

    schema = OutputFormat.model_json_schema()

    # Groq strict structured output requirement
    schema["additionalProperties"] = False

    # Fix nested objects as well
    if "$defs" in schema:

        for definition in schema["$defs"].values():

            if definition.get("type") == "object":

                definition["additionalProperties"] = False

    final_response = client.chat.completions.create(

        model=MODEL,

        messages=messages,

        response_format={
            "type": "json_schema",

            "json_schema": {

                "name": "weather_response",

                "strict": True,

                "schema": schema

            }
        }
    )

    raw_result = (
        final_response
        .choices[0]
        .message
        .content
    )

    result = json.loads(raw_result)

    return OutputFormat.model_validate(result)


# ============================================================
# DISPLAY RESULT
# ============================================================

def display_result(result: OutputFormat):

    console.print(
        "\n🤖 Assistant:\n"
    )

    for weather in result.results:

        console.print(
            Panel(
                f"""
📍 City: {weather.city}

🌡️ Temperature: {weather.temperature}

☀️ Condition: {weather.condition}

📅 Forecast:
""",
                title=f"🌤️ {weather.city}"
            )
        )

        for day in weather.forecast:

            console.print(
                f"   📅 {day.date}"
            )

            console.print(
                f"      🌡️ {day.min_temp}°C - "
                f"{day.max_temp}°C"
            )

            console.print(
                f"      ☁️ {day.description}"
            )

        console.print()


# ============================================================
# MAIN
# ============================================================

def main():

    console.print(
        Panel(
            "🌤️ Weather Agent\n"
            "Ask me about current weather or forecast.\n"
            "You can ask about multiple cities.\n"
            "Type 'exit' to quit.",
            title="🤖 Assistant"
        )
    )

    while True:

        user_query = console.input(
            "\n👤 You: "
        )

        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

        if user_query.lower().strip() in [
            "exit",
            "quit",
            "bye"
        ]:

            console.print(
                "\n🤖 Assistant: Goodbye! 👋"
            )

            break

        # ----------------------------------------------------
        # Empty input
        # ----------------------------------------------------

        if not user_query.strip():

            console.print(
                "⚠️ Please enter a question."
            )

            continue

        # ----------------------------------------------------
        # Run Agent
        # ----------------------------------------------------

        console.print(
            "\n🧠 Planning...\n"
        )

        try:

            result = run_agent(
                user_query
            )

            display_result(
                result
            )

        except Exception as e:

            console.print(
                f"\n❌ Something went wrong:\n{e}"
            )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()