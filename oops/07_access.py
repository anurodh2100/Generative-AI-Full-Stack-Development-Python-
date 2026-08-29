class Chai:
    def __init__(self,type_, strength):
        self.type = type
        self.strength = strength
        
# #code duplicationn
# class GingrChai(Chai):
#     def __ini__(self, type_, strength , spice_level):
#         self.type = type_
#         self.strength = strength
#         self.spice_level = spice_level


# #explicit call 
# class GingerChai(Chai):
#     def __init__(self,type_ , strength, spice_level):
#         Chai.__init__(self, type_ , strength)
        
#         self.spice_level = spice_level
    
    
#using super
#preffered one
class GingerCha(Chai):
    def __init__(self, type_, strength, spice_level):
        super().__init__(type_, strength)
        self.spice_level = spice_level
    