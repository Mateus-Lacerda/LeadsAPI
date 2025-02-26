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
    """Enumeração de papéis (Role)."""
    Author = auto()  # Autor
    Editor = auto()  # Editor
    Developer = auto()  # Desenvolvedor
    Admin = Author | Editor | Developer  # Admin é uma combinação de Autor, Editor e Desenvolvedor


class User(BaseModel):
    """Modelo de usuário (User)."""
    name: str = Field(examples=["Mateus"])  # Nome do usuário com um exemplo
    email: EmailStr = Field(
        examples=["mateus@ai.com"],
        description="O endereço de email do usuário",  # Descrição do campo de email
        frozen=True,  # Campo imutável após a criação
    )
    password: SecretStr = Field(
        examples=["Password123"], description="A senha do usuário"  # Descrição do campo de senha
    )
    role: Role = Field(default=None, description="O papel do usuário")  # Papel do usuário com valor padrão None


# Esta função é responsável por validar os dados fornecidos
# Aqui é usada a validação embutida do Pydantic
def validate(data: dict[str, Any]) -> None:
    """Valida os dados fornecidos."""
    try:
        user = User.model_validate(data)  # Tenta validar os dados e criar um objeto User
        print(user)  # Imprime o objeto User se a validação for bem-sucedida
    except ValidationError as errors:
        print("Usuário inválido")  # Mensagem de erro se a validação falhar
        for error in errors.errors():
            print(error)  # Imprime cada erro de validação


def main() -> None:
    """Função principal."""
    # Dados que serão validados corretamente
    good_data = {
        "name": "Mateus",
        "email": "mateus@ai.com",
        "password": "Password123",
    }
    # Dados ruins que irão gerar um erro de validação
    bad_data = {"email": "<bad data>", "password": "<bad data>"}

    validate(good_data)  # Valida dados corretos
    validate(bad_data)  # Valida dados incorretos

if __name__ == "__main__":
    main()  # Executa a função principal se o script for executado diretamente
