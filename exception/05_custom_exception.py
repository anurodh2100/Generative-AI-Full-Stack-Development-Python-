def brew_chai(flavor):
    # Check whether the flavor is available
    if flavor not in ["masala", "ginger", "elaichi"]:
        # Manually raise an exception
        raise ValueError("Unknown chai flavor!")

    print(f"☕ Brewing {flavor} chai...")


brew_chai("mint")