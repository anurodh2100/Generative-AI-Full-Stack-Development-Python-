import threading
import time


def monitor_tea_temp():

    while True:
        print(
            f"Monitoring tea temperature... "
            f"Current temp: {time.time() % 100:.2f}°C"
        )

        time.sleep(2)


# Create the thread
t = threading.Thread(
    target=monitor_tea_temp,

)

# Start the thread
t.start()

print("Main Program done! ✅")