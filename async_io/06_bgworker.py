import asyncio
import threading
import time 

def background_worker():
    while True:
        time .sleep(1)
        print(f"Loggging the system health 🕰️")
        
async def fetch_orders():
    await asyncio.sleep(3)
    print("Orders fetched! ✅")
    
threading.Thread(target=background_worker, daemon=True).start()


asyncio.run(fetch_orders())

