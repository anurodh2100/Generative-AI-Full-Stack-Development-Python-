from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    is_active: bool = True
    
    
input_data = {
    "id": 123,
    "name": "AJ",
    "is_active": False
}


user = User(**input_data)

print(user )
