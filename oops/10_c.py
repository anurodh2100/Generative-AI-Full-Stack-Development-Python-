class Chaiorder:
    
    def __init__(self, tea_type , sweetness , size):
        self.tea_type = tea_type
        self.sweetness = sweetness
        self.size = size
        
    @classmethod
    def from_dict(cls, order_data):
        return cls(
            order_data["tea_type"],
            order_data["sweetness"],
            order_data["size"]
        )
        
    @classmethod
    def from_string(cls , order_string):
        tea_type , sweetness , size = order_string.split("-")
        return cls(tea_type, sweetness , size)
    
class ChaiUtils:
    @staticmethod
    def is_valid_size(size):
        return size in ["Small", "Medium", "Large"]
    
print(ChaiUtils.is_valid_size("Medium"))
order1 = Chaiorder.from_dict({"tea_type" : "masala","sweetness":"medium", "size":"Large"})

order2 = Chaiorder.from_string("Ginger-Low-Small")

order3 = Chaiorder("Large", "Low", "Small")

    
print(order1.__dict__)
print(order2.__dict__)
print(order3.__dict__)
