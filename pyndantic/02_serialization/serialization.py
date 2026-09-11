from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime


class Address(BaseModel):
    street: str
    city: str
    zip_code: str


class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True
    createdAt: datetime
    address: Address
    tags: List[str] = []

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.strftime('%d-%m-%Y %H:%M:%S')
        }
    )


user = User(
    id=1,
    name="Amar",
    email="amar@gmail.com",
    createdAt=datetime(2026, 3, 15, 14, 30),
    address=Address(
        street="Something",
        city="Indore",
        zip_code="450066",
    ),
    is_active=False,
    tags=['premium', 'subscriber']
)

python_dump = user.model_dump()
print(user)
print("="*300)
print(python_dump)


json_str = user.model_dump_json()
print("="*300)
print(json_str)