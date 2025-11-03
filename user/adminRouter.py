from fastapi import APIRouter, Depends  , status , HTTPException  ,Request

router = APIRouter(
    prefix="/admin",       
    tags=["Admin"],        
)

@router.post("/create-slot")
async def create_slot():
    
    return {
        "message":"slot created successfully"
    }

@router.put("/update-slot")
async def create_slot():
    return {
        "message":"slot created successfully"
    }

@router.delete("/delete-slot")
async def create_slot():
    return {
        "message":"slot created successfully"
    }

@router.get("/slots")
async def create_slot():
    return {
        "message":"slot created successfully"
    }