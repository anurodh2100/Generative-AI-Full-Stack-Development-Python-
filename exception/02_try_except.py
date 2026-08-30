chai_menu = {"Masala":30, "ginger": 40}
try:
    chai_menu["elaichi"]
except KeyError:
    print("the key you are trying to find does not exist"
          )


print("hello Chai Code")
