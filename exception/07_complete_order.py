# Custom exception
class InvalidChaiError(Exception):
    pass


def bill(flavor, cups):
    """
    Demonstrates:
    1. Custom exception → InvalidChaiError
    2. Built-in exception → TypeError
    3. Exception handling → except Exception
    4. finally → always executes
    """

    menu = {
        "masala": 20,
        "ginger": 40
    }

    try:
        # Raise our custom error if chai isn't available
        if flavor not in menu:
            raise InvalidChaiError("That chai is not available!")

        # Raise built-in TypeError if cups isn't an integer
        if not isinstance(cups, int):
            raise TypeError("No. of cups must be an integer!")

        total = menu[flavor] * cups

        print(
            f"☕ Bill for {cups} cups of {flavor} chai: ₹{total}"
        )

    # Handles any exception raised inside try
    except Exception as e:
        print(f"❌ Error: {e}")

    # Always runs — error or no error
    finally:
        print("🙏 Thank you for visiting Chai!\n")


bill("mint", 2)
bill("masala", "three")
bill("masala", 30)