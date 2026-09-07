
import threading
import time

chai_stock = 0

def restock():
    global chai_stock

    for _ in range(10):
        current = chai_stock       # READ

        time.sleep(0.001)          # Give another thread a chance

        chai_stock = current + 1   # WRITE


threads = [threading.Thread(target=restock) for _ in range(2)]

for t in threads:
    t.start()

for t in threads:
    t.join()

print("Final chai stock:", chai_stock)