import asyncio
import time

async def brew(name):
    print(f"Brewing {name}.....")
    await asyncio.sleep(3)
    print(f"{name} is ready! ✅")
    
    #time.sleep(3)  # This line is commented out because it would block the event loop
    #await means wait but with non-blocking, so other tasks can run while waiting for this one to finish.

async def main():
    await asyncio.gather(
        brew("Masala Chai"),
        brew("Adrak Wali Chai"),
        brew("Elaichi Wali Chai")
    )

asyncio.run(main())