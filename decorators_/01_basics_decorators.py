from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper():
        print("Befor Functions runs")
        func()
        print("After Function runs")
    return wrapper

@my_decorator
def greet():
    print("Hello from decorators class from chaicode ")
    

greet()

print(greet.__name__)
