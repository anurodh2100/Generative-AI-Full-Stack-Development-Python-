import asyncio 
import time

from concurrent.futures import ThreadPoolExecutor 


def  check_stock(item):
    print(f"Checking stock for {item}.....")
    time.sleep(3)
    return f"{item} is in stock! ✅"
    
async def main():
        # Run the blocking function in a separate thread
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, check_stock, "Masala Chai")
        print(result)
        
        
if __name__ == "__main__":
    asyncio.run(main())