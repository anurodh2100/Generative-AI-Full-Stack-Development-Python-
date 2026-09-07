import asyncio 

async def brew_chai():
    print("Brewing Chai.....")
    await asyncio.sleep(3)
    print("Chai is ready! ✅")



asyncio.run(brew_chai())