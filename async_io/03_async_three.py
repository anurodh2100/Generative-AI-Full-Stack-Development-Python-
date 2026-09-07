import asyncio
import aiohttp


# Async function to fetch a URL
async def fetch_url(session, url):

    # session.get() makes an HTTP request asynchronously
    # "async with" automatically closes the response after we're done
    async with session.get(url) as response:

        # response.status gives the HTTP status code
        # Example: 200 = successful request
        print(f"Fetched {url} with status: {response.status}")


# Main async function
async def main():

    # Same URL repeated 3 times
    # httpbin.org/delay/3 waits approximately 3 seconds before responding
    urls = ["https://httpbin.org/delay/3"] * 3


    # Create one HTTP session
    # Reusing one session is better than creating a new session for every request
    async with aiohttp.ClientSession() as session:

        # Create a coroutine for every URL
        #
        # List comprehension:
        # for each url → call fetch_url(session, url)
        #
        # IMPORTANT:
        # fetch_url() is async, so calling it creates a coroutine.
        # It doesn't execute the request immediately.
        tasks = [fetch_url(session, url) for url in urls]


        # Run all the coroutines concurrently
        #
        # *tasks unpacks the list:
        #
        # asyncio.gather(
        #     task1,
        #     task2,
        #     task3
        # )
        #
        # "await" waits until all of them finish.
        await asyncio.gather(*tasks)


# Start the asyncio event loop
asyncio.run(main())