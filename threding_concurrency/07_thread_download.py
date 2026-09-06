import requests 
import threading    
import time 

def download(url):
    print(f"Start download from {url}")
    resp = requests.get(url)
    print(f"Finished download from {url}, size: {len(resp.content)} bytes")
    
    
urls = [
    "https://httpbin.org/image/jpeg",
    "https://httpbin.org/image/png",
    "https://httpbin.org/image/svg",
]

start = time.time()
threads = []

for url in urls:
    t = threading.Thread(target=download, args=(url,))
    t.start()
    threads.append(t)
    
for t in threads:
    t.join()
    
end = time.time()
print(f"Total time taken: {end - start:.2f} seconds")


