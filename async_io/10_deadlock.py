import threading
import time

lock_a = threading.Lock()
lock_b = threading.Lock()


def task1():
    with lock_a:
        print("Task 1 acquired lock A")

        time.sleep(1)  # Give Task 2 time to acquire lock B

        with lock_b:
            print("Task 1 acquired lock B")


def task2():
    with lock_b:
        print("Task 2 acquired lock B")

        time.sleep(1)  # Give Task 1 time to acquire lock A

        with lock_a:
            print("Task 2 acquired lock A")


t1 = threading.Thread(target=task1)
t2 = threading.Thread(target=task2)

t1.start()
t2.start()

t1.join()
t2.join()

print("Main program done!")