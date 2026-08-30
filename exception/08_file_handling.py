# file = open("order.txt","w")

# try:
#     file.write("Masala Chai - 2 cups")
# finally:
#     file.close()
    
#moder way

#same as above

with open("order.txt","w") as file :
    file.write("Giner Tea - 4 cups")
    
