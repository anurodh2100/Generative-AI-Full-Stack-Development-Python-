from typing import Optional

from pydantic import BaseModel, Field


class Employee(BaseModel):

    id: int

    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Employee name must be between 3 and 50 characters",
        examples=["Amar John"]
    )

    department: Optional[str] = "General"

    salary: float = Field(
        ...,
        gt=0,
        description="Salary must be greater than 0",
        examples=[50000.00]
    )


class User(BaseModel):

    email: str = Field(
        ...,
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",
        description="Enter a valid email address"
    )

    phone: str = Field(
        ...,
        pattern=r"^\d{10}$",
        description="Phone number must contain exactly 10 digits"
    )

    age: int = Field(
        ...,
        ge=0,
        le=150,
        description="Age in years"
    )

    discount: float = Field(
        ...,
        ge=0,
        le=100,
        description="Discount must be between 0 and 100"
    )


# Example Employee
employee = Employee(
    id=1,
    name="Amar John",
    salary=50000
)

print(employee)


# Example User
user = User(
    email="amar@gmail.com",
    phone="9876543210",
    age=25,
    discount=10
)

print(user)