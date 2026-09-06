from multiprocessing import Process, Queue, Value 

def increment(counter):
    for  _ in range(10000):
        counter.value += 1
        

if __name__ == "__main__":
    counter = Value('i', 0)
    processes = [Process(target=increment, args=(counter,)) for _ in range(4)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    print(counter.value)