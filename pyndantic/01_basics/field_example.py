from pydantic import BaseModel
from typing import List, Dict, Optional

class Cart(BaseModel):
    user_id: int
    itmes: List[str]
    quantities: Dict[str, int]
    
class BlogPost(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None
    
cart_data = {
    "user_id": 1,
    "itmes": ["Laptop", "Mouse", "Keyboard"],
    "quantities": {"Laptop": 1, "Mouse": 2, "Keyboard":3}
}

cart = Cart(**cart_data)

