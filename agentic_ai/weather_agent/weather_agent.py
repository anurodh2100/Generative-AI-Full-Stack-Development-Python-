from groq import Groq
from dotenv import load_dotenv
import os
import requests 

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def get_weather(city:str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"The Weather in {city} is {response.text}"
    
    return "Something Went wrong"

def main():

    user_query = input("🌤️ Ask about the weather: ")

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": user_query
            }
        ]
    )

    print("\n🤖 Weather Agent:")
    print(response.choices[0].message.content)



print(get_weather("Indore"))