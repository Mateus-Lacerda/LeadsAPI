"""Routes for leads."""
from fastapi import APIRouter, Query, HTTPException

from api.models.api_leads import LeadModel
from models.leads import Lead

router = APIRouter(tags=["Leads"])

@router.post("/leads", response_model=Lead)
async def create_lead(lead: Lead) -> Lead:
    """Create a lead."""
    return lead

@router.get("/leads/{lead_id}", response_model=LeadModel)
async def read_lead(lead_id: str) -> Lead:
    """Read a lead."""
    try:
        return Lead.get_lead(lead_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

@router.get("/leads", response_model=list[LeadModel])
async def read_leads(
    sort: bool = Query(False, description="Sort the leads by priority")
) -> list[Lead]:
    """Read all leads."""
    return Lead.get_lead(sort=sort)

@router.delete("/leads/{lead_id}")
async def delete_lead(lead_id: int) -> dict[str, str]:
    """Delete a lead."""
    Lead.delete_lead(lead_id)
    return {"message": "Lead deleted successfully"}
