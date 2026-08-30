class OutofIngredientsError(Exception):
    pass

def makeChai(milk, sugar):
    if milk == 0 or sugar ==0:
        raise OutofIngredientsError("Missing milk or sugar")
    print("chai is ready....")
    
    
makeChai(0,2)