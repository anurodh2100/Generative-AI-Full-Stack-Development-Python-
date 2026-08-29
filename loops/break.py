#out of order.py


flavours = ["Ginger", "Out of Stock","Lemon", "Discontinued", "tulsi"]

for flavour in flavours:
    if flavour == "Out of Stock":
        continue
    if flavour == "Discontinued":
        break
    print("Discountinued item found")

print(f"Out side of loop")