"""Pydantic examples."""
import hashlib  # Importa a biblioteca hashlib para hashing de senhas
import re  # Importa a biblioteca re para expressões regulares
from enum import IntFlag  # Importa IntFlag para criar enums
from typing import Any  # Importa Any para tipagem

from pydantic import (
    BaseModel,  # Importa BaseModel para criar modelos Pydantic
    EmailStr,  # Importa EmailStr para validação de emails
    Field,  # Importa Field para definir campos do modelo
    SecretStr,  # Importa SecretStr para campos de senha
    ValidationError,  # Importa ValidationError para tratar erros de validação
    field_validator,  # Importa field_validator para validar campos individualmente
    model_validator,  # Importa model_validator para validar o modelo como um todo
)

# Este regex verifica se a senha contém pelo menos 8 caracteres,
# uma letra maiúscula, uma letra minúscula e um número
VALID_PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")
# Este regex verifica se o nome contém apenas letras e tem pelo menos 2 caracteres
VALID_NAME_REGEX = re.compile(r"^[a-zA-Z]{2,}$")


class Role(IntFlag):
    """Role enum."""
    Author = 1  # Define o papel de Autor
    Editor = 2  # Define o papel de Editor
    Admin = 4  # Define o papel de Admin
    SuperAdmin = 8  # Define o papel de SuperAdmin


class User(BaseModel):
    """User model."""
    name: str = Field(examples=["Mateus"])  # Nome do usuário com exemplo
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
        if not VALID_NAME_REGEX.match(v):  # Verifica se o nome é válido
            raise ValueError(
                "Name is invalid, must contain only letters and have at least 2 characters"
            )
        return v

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, v: int | str | Role) -> Role:
        """Validate role."""
        op = {int: lambda x: Role(x), str: lambda x: Role[x], Role: lambda x: x}  # Mapeia tipos para Role
        try:
            return op[type(v)](v)  # Converte o valor para Role
        except (KeyError, ValueError) as error:
            raise ValueError(
                f"Role is invalid, please use one of {', '.join(x.name for x in Role)}"
            ) from error

    @model_validator(mode="before")
    @classmethod
    def validate_user(cls, v: dict[str, Any]) -> dict[str, Any]:
        """Validate user."""
        if "name" not in v or "password" not in v:  # Verifica se nome e senha estão presentes
            raise ValueError("Name and password are required")
        if v["name"].casefold() in v["password"].casefold():  # Verifica se a senha contém o nome
            raise ValueError("Password should not contain the name")
        if not VALID_PASSWORD_REGEX.match(v["password"]):  # Verifica se a senha é válida
            raise ValueError(
                "Password is invalid, must contain at least 8 characters, "
                "one uppercase letter, one lowercase letter and one number"
            )
        # Hash the password using SHA-256
        v["password"] = hashlib.sha256(v["password"].encode()).hexdigest()  # Faz o hash da senha
        return v

def validade(data: dict[str, Any]) -> None:
    """Validate data."""
    try:
        user = User.model_validate(data)  # Valida os dados e cria um objeto User
        print(user)  # Imprime o objeto User
    except ValidationError as errors:
        print("User is invalid")  # Mensagem de erro se a validação falhar
        for error in errors.errors():
            print(error)  # Imprime cada erro de validação

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
        print(f"Testing {example_name}")  # Imprime o nome do exemplo sendo testado
        validade(data)  # Valida os dados do exemplo
        print()  # Imprime uma linha em branco para separar os resultados


if __name__ == "__main__":
    main()  # Executa a função principal se o script for executado diretamente
