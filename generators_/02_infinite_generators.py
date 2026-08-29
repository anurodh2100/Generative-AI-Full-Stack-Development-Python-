def infinite_chai():
    count = 1 
    while True:
        yield f"Refil #{count}"
        count +=1
    
refil = infinite_chai()
user2= infinite_chai()
for _ in range(5):
    print(next(refil))
    
print("\n")

for _ in range(6):
    print(next(user2))
    
    