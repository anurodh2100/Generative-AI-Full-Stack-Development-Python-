def process_order(item, quantity):
    """
    Demonstrates multiple except blocks.

    FLOW:
    try → execute code
    error → matching except runs

    KeyError  → item not in menu
    TypeError → quantity has wrong data type
    """

    try:
        menu = {
            "masala": 20,
            "ginger": 25,
            "elaichi": 30
        }

        price = menu[item]

        # Manually raise TypeError if quantity isn't a number
        if not isinstance(quantity, (int, float)):
            raise TypeError("Quantity must be a number")

        cost = price * quantity

        print(f"☕ {item.capitalize()} chai × {quantity}")
        print(f"💰 Total cost: ₹{cost}")

    except KeyError:
        print(f"❌ Sorry, {item} chai is not on the menu.")

    except TypeError as error:
        print(f"❌ {error}")


process_order("ginger", 2)
process_order("masala", "two")
process_order("chocolate", 2)