# ---------------------------------------------------------
# Coding Problem Solver
# Few-Shot + Planning + JSON Output + Memory + Rich
# ---------------------------------------------------------

from groq import Groq
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
import os
import json
import time


# Load environment variables
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

console = Console()


# ---------------------------------------------------------
# System Prompt
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are an expert Coding/DSA Assistant.

Return ONLY valid JSON:

{
  "start": "Brief problem understanding",
  "plan": ["step 1", "step 2"],
  "options": [
    {
      "approach": "name",
      "time": "O(...)",
      "space": "O(...)"
    }
  ],
  "optimal": "Best approach and brief reason",
  "output": {
    "code": "final code",
    "time": "O(...)",
    "space": "O(...)"
  }
}

Rules:
- Give 2-3 possible approaches.
- Compare time and space complexity.
- Select the optimal approach.
- Use requested language; otherwise Python.
- Handle important edge cases.
- Keep reasoning concise.
- Do not reveal private chain-of-thought.
- If user asks only for a hint, provide only a hint.
- For non-coding questions, politely refuse in JSON.

Example:

User: Find the largest element in an array.

Assistant:
{
  "start": "Find the largest element.",
  "plan": [
    "Initialize the maximum.",
    "Traverse the array and update it when needed."
  ],
  "options": [
    {
      "approach": "Sorting",
      "time": "O(n log n)",
      "space": "O(1)"
    },
    {
      "approach": "Linear Scan",
      "time": "O(n)",
      "space": "O(1)"
    }
  ],
  "optimal": "Linear Scan because it is O(n) and avoids sorting.",
  "output": {
    "code": "mx = arr[0]\\nfor x in arr:\\n    mx = max(mx, x)\\nprint(mx)",
    "time": "O(n)",
    "space": "O(1)"
  }
}
"""


# ---------------------------------------------------------
# Memory
# ---------------------------------------------------------

MEMORY_FILE = "memory.json"

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
# Continuous Chatbot
# ---------------------------------------------------------

console.print(
    Panel(
        "[bold]Coding Problem Solver[/bold]\n"
        "Type [yellow]exit[/yellow] to quit.",
        title="🤖 Assistant"
    )
)


while True:

    user_prompt = console.input("\n[bold cyan]You:[/bold cyan] ")

    # Exit chatbot
    if user_prompt.strip().lower() == "exit":
        console.print("[bold green]Assistant:[/bold green] Goodbye! 👋")
        break


    # Add user message
    messages.append({
        "role": "user",
        "content": user_prompt
    })


    # Start timer
    start_time = time.perf_counter()


    # -----------------------------------------------------
    # API Call
    # -----------------------------------------------------

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        response_format={
            "type": "json_object"
        }
    )


    # Response time
    response_time = time.perf_counter() - start_time


    # Get response
    answer = response.choices[0].message.content


    # Add assistant response to memory
    messages.append({
        "role": "assistant",
        "content": answer
    })


    # Save memory
    with open(MEMORY_FILE, "w") as f:
        json.dump(messages, f, indent=4)


    # -----------------------------------------------------
    # Display JSON nicely
    # -----------------------------------------------------

    try:
        data = json.loads(answer)

        console.print("\n[bold green]START[/bold green]")
        console.print(data.get("start", ""))

        console.print("\n[bold yellow]PLAN[/bold yellow]")
        for step in data.get("plan", []):
            console.print(f"• {step}")

        console.print("\n[bold magenta]OPTIONS[/bold magenta]")

        for option in data.get("options", []):
            console.print(
                f"• [bold]{option['approach']}[/bold] | "
                f"Time: {option['time']} | "
                f"Space: {option['space']}"
            )

        console.print("\n[bold blue]OPTIMAL[/bold blue]")
        console.print(data.get("optimal", ""))

        output = data.get("output", {})

        console.print("\n[bold green]OUTPUT[/bold green]")

        console.print(
            Syntax(
                output.get("code", ""),
                "python",
                theme="monokai",
                line_numbers=True
            )
        )

        console.print(
            f"\nTime: {output.get('time', '')}"
        )

        console.print(
            f"Space: {output.get('space', '')}"
        )

    except json.JSONDecodeError:
        # Fallback if model somehow returns invalid JSON
        console.print(answer)


    console.print(
        f"\n[dim]Response Time: {response_time:.2f}s[/dim]"
    )