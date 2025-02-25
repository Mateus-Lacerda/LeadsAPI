"""Pydantic examples."""
import hashlib
import re
from enum import IntFlag
from typing import Any

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    SecretStr,
    ValidationError,
    field_validator,
    model_validator,
)

VALID_PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")
VALID_NAME_REGEX = re.compile(r"^[a-zA-Z]{2,}$")


class Role(IntFlag):
    """Role enum."""
    Author = 1
    Editor = 2
    Admin = 4
    SuperAdmin = 8


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
    role: Role = Field(
        default=None, description="The role of the user", examples=[1, 2, 4, 8]
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate name."""
        if not VALID_NAME_REGEX.match(v):
            raise ValueError(
                "Name is invalid, must contain only letters and have at least 2 characters"
            )
        return v

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, v: int | str | Role) -> Role:
        """Validate role."""
        op = {int: lambda x: Role(x), str: lambda x: Role[x], Role: lambda x: x}
        try:
            return op[type(v)](v)
        except (KeyError, ValueError) as error:
            raise ValueError(
                f"Role is invalid, please use one of {', '.join(x.name for x in Role)}"
            ) from error

    @model_validator(mode="before")
    @classmethod
    def validate_user(cls, v: dict[str, Any]) -> dict[str, Any]:
        """Validate user."""
        if "name" not in v or "password" not in v:
            raise ValueError("Name and password are required")
        if v["name"].casefold() in v["password"].casefold():
            raise ValueError("Password should not contain the name")
        if not VALID_PASSWORD_REGEX.match(v["password"]):
            raise ValueError(
                "Password is invalid, must contain at least 8 characters, "
                "one uppercase letter, one lowercase letter and one number"
            )
        v["password"] = hashlib.sha256(v["password"].encode()).hexdigest()
        return v

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
    test_data = dict(
        good_data={
            "name": "Mateus",
            "email": "mateus@ai.com",
            "password": "Password123",
            "role": "Admin",
        },
        bad_role={
            "name": "Mateus",
            "email": "mateus@ai.com",
            "password": "Password123",
            "role": "Programmer",
        },
        bad_data={
            "name": "Mateus",
            "email": "bad email",
            "password": "bad password",
        },
        bad_name={
            "name": "Mateus12<¬_¬>",
            "email": "mateus@ai.com",
            "password": "Password123",
        },
        duplicate={
            "name": "Mateus",
            "email": "mateus@ai.com",
            "password": "MateusPassword123",
        },
        missing_data={
            "email": "<bad data>",
            "password": "<bad data>",
        },
    )

    for example_name, data in test_data.items():
        print(f"Testing {example_name}")
        validade(data)
        print()


if __name__ == "__main__":
    main()
