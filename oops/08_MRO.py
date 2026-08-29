class A:
    label = "A : Base Class"
    
class B(A):
    label = "B : Masala Blend"
    
class C(A):
    label = "C : herbal Blend"
    
class D(B,C): #first class gets called
    pass

cup = D()
print(cup.label)
print(D.__mro__)