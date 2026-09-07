import asyncio 
from concurrent.futures import ThreadPoolExecutor

def encrypt(data):
    return f"🔒 {data[::-1]}"


async def main():
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        # Run the blocking function in a separate thread
        result = await loop.run_in_executor(pool, encrypt, "Hello, World!")
        print(f"{result}")

if __name__ == "__main__":
    asyncio.run(main())