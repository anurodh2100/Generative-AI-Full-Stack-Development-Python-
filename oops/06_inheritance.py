# Base class for all types of Chai
class BaseChai : 
     
    # Constructor
    # It runs automatically when we create an object
    def __init__(self, type_): 
        # Store the chai type inside the object
        self.type = type_ 
     
    # Method to prepare chai
    def prepare(self): 
        print(f"Preparing {self.type} chai.....") 
         
         
# MasalaChai inherits from BaseChai
# Therefore, MasalaChai gets __init__() and prepare() from BaseChai
class MasalaChai(BaseChai): 
    
    # Extra method specific to MasalaChai
    def add_spices(self): 
        print("Adding Cardamom, ginger ,cloves") 
         
 
# ChaiShop class
class ChaiShop: 
    
    # Class attribute
    # By default, this shop will use BaseChai
    chai_cls = BaseChai 
     
    def __init__(self): 
        # self.chai_cls refers to the chai class defined above
        #
        # For ChaiShop:
        # self.chai_cls = BaseChai
        # So this creates: BaseChai("Regular")
        #
        # IMPORTANT:
        # chai_cls is a CLASS, so we can call it like a constructor
        self.chai = self.chai_cls("Regular") 
         
    def serve(self): 
        # Access the type stored inside the chai object
        print(f"Serving {self.chai.type} chai in the shop") 
        
        # Call prepare() of the chai object
        self.chai.prepare() 
         
 
# FancyChaiShop inherits from ChaiShop
class FancyChaiShop(ChaiShop): 
    
    # Here we OVERRIDE the inherited class attribute
    #
    # ChaiShop:
    #     chai_cls = BaseChai
    #
    # FancyChaiShop:
    #     chai_cls = MasalaChai
    #
    # Therefore, FancyChaiShop will create MasalaChai objects
    chai_cls = MasalaChai 
     
 
# Create a normal ChaiShop object
shop = ChaiShop() 

# Since ChaiShop.chai_cls = BaseChai,
# this creates:
# shop.chai = BaseChai("Regular")
fancy = FancyChaiShop() 

# Calls ChaiShop.serve()
# shop.chai is a BaseChai object
shop.serve() 

# Calls inherited serve() method from ChaiShop
# BUT fancy.chai is a MasalaChai object
#
# Why?
# Because FancyChaiShop changed chai_cls from BaseChai to MasalaChai
fancy.serve() 

# MasalaChai has its own add_spices() method
# So we can call it using fancy.chai
fancy.chai.add_spices()