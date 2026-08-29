class TeaLeaf: 
    def __init__(self, age): 
        self.age = age       # setter is called here
         
    @property 
    def age(self): 
        return self._age + 2 
     
    @age.setter 
    def age(self, age): 
        if 1 <= age <= 5: 
            self._age = age     
        else: 
            raise ValueError("Tea age must be b/w 1 and 5 years") 
         
leaf = TeaLeaf(4)
print(leaf.age)