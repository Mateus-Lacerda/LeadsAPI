"""Pydantic examples."""
from enum import auto, IntFlag
from typing import Any

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    SecretStr,
    ValidationError,
)


class Role(IntFlag):
    """Role enum."""
    Author = auto()
    Editor = auto()
    Developer = auto()
    Admin = Author | Editor | Developer


class User(BaseModel):
    """User model."""
    name: str = Field(examples=["Mateus"])
    email: EmailStr = Field(
        examples=["mateus@ai.com"],
        description="Them email address of the user",
        frozen=True,
    )
    password: SecretStr = Field(
        examples=["Password123"], description="The password of the user"
    )
    role: Role = Field(default=None, description="The role of the user")


def validade(data: dict[str, Any]) -> None:
    """Validate data."""
    try:
        user = User.model_validate(data)
        print(user)
    except ValidationError as errors:
        print("User is invalid")
        for error in errors.errors():
            print(error)

def main() -> None:
    """Main function."""
    good_data = {
        "name": "Mateus",
        "email": "mateus@ai.com",
        "password": "Password123",
    }
    bad_data = {"email": "<bad data>", "password": "<bad data>"}

    validade(good_data)
    validade(bad_data)

if __name__ == "__main__":
    main()
