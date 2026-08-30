def serve_chai(flavor):
    try:
        print(f"🍵 Preparing {flavor} chai...")

        if flavor == "unknown":
            raise ValueError("We don't know that flavor!")

    except ValueError as error:
        print(f"❌ Error: {error}")

    else:
        print(f"✅ {flavor} chai is served!")

    finally:
        print("👤 Next customer, please!\n")


# Customers
serve_chai("masala")
serve_chai("unknown")