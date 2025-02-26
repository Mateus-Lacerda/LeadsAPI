from datetime import datetime

import pytest

from ..models import leads

def test_hot_lead_from_lead() -> None:
    # Exemplo 2: Criar um Lead com todos os campos preenchidos, que será transformado em HotLead
    try:
        full_lead = leads.Lead(
            name="Bob",
            email="bob@mail.com",
            address="Rua das Flores, 200",
            phone="+5511888888888",
            last_contact=datetime.now(),
            interests=[leads.Products.COMMERCIAL_PROPERTY, leads.Products.LAND]
        )
        assert full_lead.priority == leads.Priority.High, "Priority should be High"
        assert full_lead.lead_type == leads.LeadType.Hot, "Lead type should be Hot"
        assert full_lead.model_dump() in leads.Lead.__leads__.values(), \
            "Lead should be in the list of leads"
        try:
            leads.HotLead(**full_lead.model_dump())
            raise AssertionError("HotLead should already exist")
        except leads.ValidationError as error:
            assert True
            assert "Lead already exists" in str(error)
    except Exception as e:
        raise AssertionError(f"Error creating Lead: {e}") from e

def test_warm_lead() -> None:
    # Exemplo 3: Tentar criar um Lead com campos faltantes (deve ser transformado em WarmLead)
    try:
        incomplete_lead = leads.Lead(
            name="Charlie",
            email="charlie@mail.com",
            address=None,  # Campo faltante
            phone="+5511777777777",
            last_contact=datetime.now(),
            interests=[leads.Products.TWO_ROOM_APARTMENT, leads.Products.THREE_ROOM_HOUSE]
        )
        assert incomplete_lead.priority == leads.Priority.Medium, "Priority should be Medium"
        assert incomplete_lead.lead_type == leads.LeadType.Warm, "Lead type should be Warm"
        assert incomplete_lead.model_dump() in leads.Lead.__leads__.values(), \
            "Lead should be in the list of leads"
    except Exception as e:
        raise AssertionError(f"Error creating Lead: {e}") from e

def test_warm_lead_no_interests() -> None:
    # Exemplo 4: Criar um Lead sem interesses (deve ser transformado em WarmLead)
    try:
        incomplete_lead = leads.Lead(
            name="Mike",
            email="mike@mail.com",
            address="Rua das Flores, 200",
            phone="+5511777777777",
            last_contact=datetime.now()
        )
        assert incomplete_lead.priority == leads.Priority.Medium, "Priority should be Medium"
        assert incomplete_lead.lead_type == leads.LeadType.Warm, "Lead type should be Warm"
        assert incomplete_lead.model_dump() in leads.Lead.__leads__.values(), \
            "Lead should be in the list of leads"
    except Exception as e:
        raise AssertionError(f"Error creating Lead: {e}") from e

def test_cold_lead() -> None:
    # Exemplo 5: Criar um Lead com campos faltantes (deve ser transformado em ColdLead)
    try:
        cold_lead = leads.Lead(
            name="David",
            email=None,
            address=None,
            phone="+5511666666666",
            last_contact=datetime.now()
        )
        assert cold_lead.priority == leads.Priority.Low, "Priority should be Low"
        assert cold_lead.lead_type == leads.LeadType.Cold, "Lead type should be Cold"
        assert cold_lead.model_dump() in leads.Lead.__leads__.values(), \
            "Lead should be in the list of leads"
    except Exception as e:
        raise AssertionError(f"Error creating Lead: {e}") from e

def main() -> None:
    pytest.main(["-v", __file__])
