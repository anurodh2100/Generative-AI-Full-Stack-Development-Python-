from groq import Groq
from dotenv import load_dotenv

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

import os
import json


# =========================
# SETUP
# =========================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

console = Console()


# =========================
# SYSTEM PROMPT
# =========================

SYSTEM_PROMPT = """
You are an expert AI Assistant.

You can handle both general conversation and coding/DSA questions.

First decide whether the user's query is:

1. "chat" → greetings, general conversation, normal questions
2. "coding" → programming, DSA, algorithms, debugging, code-related questions

For "chat", return:

{
    "type": "chat",
    "response": "normal conversational answer"
}

For "coding", return:

{
    "type": "coding",
    "start": "Brief problem understanding",
    "plan": [
        "step 1",
        "step 2"
    ],
    "approach": "Best approach",
    "complexity": {
        "time": "O(...)",
        "space": "O(...)"
    },
    "code": "final code"
}

For coding questions:
- Understand the problem
- Identify the key observation
- Find a suitable approach
- Analyze time and space complexity
- Select the best approach
- Provide the final solution

Give only a concise reasoning summary.
Do not reveal private chain-of-thought.

Use Python unless another language is requested.

Return ONLY valid JSON.
"""


# =========================
# MESSAGE HISTORY
# =========================

message_history = []

message_history.append({
    "role": "system",
    "content": SYSTEM_PROMPT
})


# =========================
# CHATBOT
# =========================

console.print(
    Panel(
        "[bold]AI Coding & Chat Assistant[/bold]\n"
        "Ask anything or type [yellow]exit[/yellow] to quit.",
        title="🤖 Assistant",
        border_style="blue"
    )
)


while True:

    # 👤 User input
    user_query = console.input(
        "\n[bold cyan]👤 You:[/bold cyan] "
    )

    if user_query.strip().lower() == "exit":

        console.print(
            Panel(
                "Goodbye! 👋",
                title="🤖 Assistant",
                border_style="green"
            )
        )

        break


    # Add user message
    message_history.append({
        "role": "user",
        "content": user_query
    })


    # Send complete message history
    messages = message_history

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        response_format={
            "type": "json_object"
        }
    )


    # Raw LLM response
    raw_result = response.choices[0].message.content


    # Add assistant response to history
    message_history.append({
        "role": "assistant",
        "content": raw_result
    })


    # Parse JSON
    try:

        parsed_result = json.loads(raw_result)

    except json.JSONDecodeError:

        console.print(
            Panel(
                raw_result,
                title="🤖 Assistant",
                border_style="red"
            )
        )

        continue


    # =========================
    # GENERAL CHAT
    # =========================

    if parsed_result.get("type") == "chat":

        console.print(
            Panel(
                parsed_result.get("response", ""),
                title="🤖 Assistant",
                border_style="green"
            )
        )


    # =========================
    # CODING / DSA
    # =========================

    elif parsed_result.get("type") == "coding":

        # 🚀 START
        console.print(
            Panel(
                parsed_result.get("start", ""),
                title="🚀 START",
                border_style="blue"
            )
        )


        # 📝 PLAN
        plan = parsed_result.get("plan", [])

        plan_text = "\n".join(
            f"• {step}"
            for step in plan
        )

        console.print(
            Panel(
                plan_text,
                title="📝 PLAN",
                border_style="yellow"
            )
        )


        # 💡 APPROACH
        console.print(
            Panel(
                parsed_result.get("approach", ""),
                title="💡 APPROACH",
                border_style="magenta"
            )
        )


        # ⚡ COMPLEXITY
        complexity = parsed_result.get(
            "complexity",
            {}
        )

        complexity_text = (
            f"⏱️ Time  : {complexity.get('time', '')}\n"
            f"💾 Space : {complexity.get('space', '')}"
        )

        console.print(
            Panel(
                complexity_text,
                title="⚡ COMPLEXITY",
                border_style="cyan"
            )
        )


        # 💻 CODE
        code = parsed_result.get("code", "")

        console.print(
            Panel(
                Syntax(
                    code,
                    "python",
                    theme="monokai",
                    line_numbers=True
                ),
                title="💻 CODE",
                border_style="green"
            )
        )