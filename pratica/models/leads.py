"""Module for the Leads Models"""
from datetime import datetime
from enum import Enum, IntEnum
from typing import Any, Optional
from uuid import uuid4

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ValidationError,
    model_validator,
)


class Priority(IntEnum):
    """Priority of the lead"""
    Low = 1
    Medium = 2
    High = 4

class LeadType(Enum):
    """Type of the lead"""
    Cold = "cold"
    Warm = "warm"
    Hot = "hot"

class StringID(str):
    """String ID for the lead"""
    def __new__(cls) -> str:
        return str(uuid4())

class Products(Enum):
    """Products that the lead is interested in"""
    TWO_ROOM_APARTMENT = "two_room_apartment"
    THREE_ROOM_APARTMENT = "three_room_apartment"
    TWO_ROOM_HOUSE = "two_room_house"
    THREE_ROOM_HOUSE = "three_room_house"
    FOUR_ROOM_HOUSE = "four_room_house"
    POOL_HOUSE = "pool_house"
    DUPLEX = "duplex"
    PENTHOUSE = "penthouse"
    COMMERCIAL_PROPERTY = "commercial"
    LAND = "land"

class HotLead(BaseModel):
    """Hot Lead Model, used for hot leads"""
    name: str = Field(examples=["Example"])
    email: EmailStr = Field(
        examples=["example@mail.com"],
        description="The email address of the lead",
        frozen=True,
    )
    address: str = Field(
        examples=["123 Example St"],
        description="The address of the lead",
    )
    phone: str = Field(
        examples=["+1234567890"],
        description="The phone number of the lead",
    )
    interests: list[Products] = Field(
        examples=[[Products.TWO_ROOM_APARTMENT, Products.THREE_ROOM_HOUSE]],
        description="The products that the lead is interested in",
    )
    priority: Priority = Field(
        description="The priority of the lead",
        examples=[4],
        default=4,
        validate_default=True,
    )
    lead_type: LeadType = Field(
        description="The type of the lead",
        examples=["hot"],
        default="hot",
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

    @model_validator(mode="before")
    @classmethod
    def qualify(cls, v: dict[str, Any]) -> "HotLead":
        """Qualify the lead"""
        if v["priority"] != Priority.High:
            raise ValueError("Hot leads must have a high priority")
        if v["lead_type"] != LeadType.Hot:
            raise ValueError("Hot leads must have a hot lead type")
        if any(
            v["email"] == lead["email"]
            for lead in Lead.__leads__.values()
        ):
            raise ValueError("Lead already exists")
        return v

    def model_post_init(self, __context: dict[str, Any]) -> None:
        """Adds the valid lead to the list of leads"""
        Lead.__leads__[self.lead_id] = self.model_dump()

class Lead(BaseModel):
    """Base Lead Model, used for warm and cold leads"""
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

    @model_validator(mode="before")
    @classmethod
    def validate_lead(cls, v: dict[str, Any]) -> "Lead":
        """Validate the lead"""
        required_for_warm = [
            "name",
            "email"
        ]
        if any(
            v[required] is None
            for required in required_for_warm
        ):
            v["priority"] = Priority.Low
            v["lead_type"] = LeadType.Cold
        else:
            v["priority"] = Priority.Medium
            v["lead_type"] = LeadType.Warm
        return v

    def analize_quality(self) -> Optional["Lead"]:
        """Qualify the lead"""
        if self.priority == Priority.Low and self.lead_type == LeadType.Cold:
            return self
        if self.interests:
            try:
                self.priority = Priority.High
                self.lead_type = LeadType.Hot
                HotLead(**self.model_dump())
                return
            except ValidationError:
                self.priority = Priority.Medium
                self.lead_type = LeadType.Warm
                return self
        return self

    def model_post_init(self, __context: dict[str, Any]) -> None:
        """Adds the valid lead to the list of leads"""
        lead = self.analize_quality()
        if lead:
            if any(
                lead.email == stored_lead["email"]
                for stored_lead in self.__leads__.values()
            ):
                raise ValueError("Lead already exists")
            self.__class__.__leads__[self.lead_id] = lead.model_dump()

    def get_lead(
            lead_id: str | None = None, sort: bool = False
            ) -> dict[str, dict] | list[dict[str, dict]]:
        """Get a lead by its ID"""
        if sort:
            return sorted(
                Lead.__leads__.values(), key=lambda x: x["priority"], reverse=True
            )
        if not lead_id:
            return list(Lead.__leads__.values())
        if lead_id not in Lead.__leads__.keys():
            raise ValueError("Lead not found")
        return Lead.__leads__[lead_id]

    def delete_lead(lead_id: str) -> None:
        """Delete a lead by its ID"""
        del Lead.__leads__[lead_id]
