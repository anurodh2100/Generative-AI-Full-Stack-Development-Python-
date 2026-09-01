import threading 
import time

def prepare_cai(type_, wait_time):
    print(f"{type_} chai : brewing ....")
    time.sleep(wait_time)
    print(f"{type_} chai : Ready ....")
    
    
t1 = threading.Thread(target=prepare_cai, args=("Masala", 3))
t2 = threading.Thread(target=prepare_cai, args=("Ginger", 2))

t1.start()
t2.start()
t1.join()
t2.join()


