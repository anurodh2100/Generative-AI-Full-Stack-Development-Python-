class Chai:
    temperature = "hot"
    strength = "Strong"
    
cutting = Chai()
print(cutting.temperature)

cutting.temperature = "Mild"
cutting.cup = "small"
print("After Chaging : ", cutting.temperature)
print("Direct Look into class ", Chai.temperature)
print("the cup size is "cutting.cup)

del cutting.temperature

print(cutting.temperature)