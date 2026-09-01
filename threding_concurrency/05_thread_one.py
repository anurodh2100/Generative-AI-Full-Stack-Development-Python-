import threading 
import time 

def boil_milk():
    print(f"boiling milk ............")
    time.sleep(2)
    print(f"Milk Boiled.....")
    
def toast_bun():
    print(f"toasting bun ............")
    time.sleep(3)
    print(f"Done with Bun Toast.....")

boil_milk()
toast_bun()

start = time.time()
thread1 = threading.Thread(target=boil_milk)
thread2 = threading.Thread(target=toast_bun)

thread1.start()
thread2.start()
thread1.join()
thread2.join()

end = time.time()

print(f"Total time taken: {end - start:.2f} seconds")