from functools import wraps
from datetime import datetime


def log_activity(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()

        print(f"🔵 Starting: {func.__name__}")

        try:
            result = func(*args, **kwargs)

            duration = (datetime.now() - start_time).total_seconds()

            print(f"🟢 Finished: {func.__name__} ({duration:.2f}s)")
            return result

        except Exception as e:
            print(f"🔴 Failed: {func.__name__} → {e}")
            raise

    return wrapper


@log_activity
def brew_chai(chai_type):
    print(f"☕ Brewing {chai_type} chai")


brew_chai("Masala")