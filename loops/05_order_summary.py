names = ["Hitesh", "Meera", "Rahul"]
bills = [50,60,100]

#zip list 

for item in zip(names, bills):
    print(f"{item[0]}: INR {item[1]}")