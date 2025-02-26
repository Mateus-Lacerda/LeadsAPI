import enum
import hashlib
import re
from typing import Any, Self
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_serializer,
    field_validator,
    model_serializer,
    model_validator,
    SecretStr,
)

# Regex para validar a senha
VALID_PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
# Regex para validar o nome
VALID_NAME_REGEX = re.compile(r"^[a-zA-Z]{2,}$")

# Definição das diferentes funções de usuário usando IntFlag para permitir combinações
class Role(enum.IntFlag):
    User = 0
    Author = 1
    Editor = 2
    Admin = 4
    SuperAdmin = 8

# Modelo de dados do usuário usando Pydantic
class User(BaseModel):
    name: str = Field(examples=["Example"])  # Nome do usuário com exemplo
    email: EmailStr = Field(
        examples=["user@arjancodes.com"],
        description="The email address of the user",
        frozen=True,
    )
    password: SecretStr = Field(
        examples=["Password123"], description="The password of the user", exclude=True
    )
    role: Role = Field(
        description="The role of the user",
        examples=[1, 2, 4, 8],
        default=0,
        validate_default=True,
    )

    # Validador para o campo 'name'
    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        if not VALID_NAME_REGEX.match(v):
            raise ValueError(
                "Name is invalid, must contain only letters and be at least 2 characters long"
            )
        return v

    # Validador para o campo 'role' antes da validação do modelo
    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, v: int | str | Role) -> Role:
        op = {int: lambda x: Role(x), str: lambda x: Role[x], Role: lambda x: x}
        try:
            return op[type(v)](v)
        except (KeyError, ValueError) as error:
            raise ValueError(
                "Role is invalid, please use one of the following: "
                f"{', '.join([x.name for x in Role])}"
            ) from error

    # Validador do modelo antes da criação do objeto
    @model_validator(mode="before")
    @classmethod
    def validate_user_pre(cls, v: dict[str, Any]) -> dict[str, Any]:
        if "name" not in v or "password" not in v:
            raise ValueError("Name and password are required")
        if v["name"].casefold() in v["password"].casefold():
            raise ValueError("Password cannot contain name")
        if not VALID_PASSWORD_REGEX.match(v["password"]):
            raise ValueError(
                "Password is invalid, must contain 8 characters, 1 uppercase, 1 lowercase, 1 number"
            )
        v["password"] = hashlib.sha256(v["password"].encode()).hexdigest()
        return v

    # Validador do modelo após a criação do objeto
    @model_validator(mode="after")
    def validate_user_post(self, v: Any) -> Self:
        if self.role == Role.Admin and self.name != "Arjan":
            raise ValueError("Only Arjan can be an admin")
        return self

    # Serializador para o campo 'role' quando usado em JSON
    @field_serializer("role", when_used="json")
    @classmethod
    def serialize_role(cls, v: Any) -> str:
        return v.name

    # Serializador do modelo quando usado em JSON
    @model_serializer(mode="wrap", when_used="json")
    def serialize_user(self, serializer, info) -> dict[str, Any]:
        if not info.include and not info.exclude:
            return {"name": self.name, "role": self.role.name}
        return serializer(self)

# Função principal para testar a validação e serialização do modelo User
def main() -> None:
    data = {
        "name": "Arjan",
        "email": "example@arjancodes.com",
        "password": "Password123",
        "role": "Admin",
    }
    user = User.model_validate(data)  # Valida os dados e cria um objeto User
    if user:
        print(
            "The serializer that returns a dict:",
            user.model_dump(),
            sep="\n",
            end="\n\n",
        )
        print(
            "The serializer that returns a JSON string:",
            user.model_dump(mode="json"),
            sep="\n",
            end="\n\n",
        )
        print(
            "The serializer that returns a json string, excluding the role:",
            user.model_dump(exclude=["role"], mode="json"),
            sep="\n",
            end="\n\n",
        )
        print("The serializer that encodes all values to a dict:", dict(user), sep="\n")

# Executa a função principal se o script for executado diretamente
if __name__ == "__main__":
    main()
