
from fastapi import APIRouter

router_company = APIRouter()

@router_company.get("/")
async def get_company_name():
    return {"company name": "Example Company. LLC"}

@router_company.get("/employees")
async def number_of_employees():
    return {"employees number":160}