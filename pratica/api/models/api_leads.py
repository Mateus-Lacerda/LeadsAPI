from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
    Field
)

from models.leads import Priority, Products, LeadType, StringID


class LeadModel(BaseModel):
    """Lead Model for the API, used for warm and cold leads"""
    __leads__: dict[str, dict] = {}
    name: str | None = Field(examples=["Example"])
    email: EmailStr | None = Field(
        examples=["example@mail.com"],
        description="The email address of the lead",
        frozen=True,
    )
    address: str | None = Field(
        examples=["123 Example St"],
        description="The address of the lead",
    )
    phone: str | None = Field(
        examples=["+1234567890"],
        description="The phone number of the lead",
    )
    interests: list[Products] | None = Field(
        examples=[[Products.TWO_ROOM_APARTMENT, Products.THREE_ROOM_HOUSE]],
        description="The products that the lead is interested in",
        default=None,
    )
    priority: Priority = Field(
        description="The priority of the lead",
        examples=[1, 2],
        default=1,
        validate_default=True,
    )
    lead_type: LeadType = Field(
        description="The type of the lead",
        examples=["cold", "warm", "hot"],
        default="cold",
        validate_default=True,
    )
    last_contact: datetime | None = Field(
        description="The last time the lead has made contact",
        examples=[datetime.now().timestamp()],
    )
    lead_id: str = Field(
        description="The unique identifier of the lead",
        examples=[StringID()],
        default_factory=StringID,
    )
