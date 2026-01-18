from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # PRO: Per lidhje me Frontend
from pydantic import BaseModel, Field # PRO: Per validim te numrave
from typing import Optional

try:
    from solver import solve_schedule 
except ImportError:
    def solve_schedule(capacity, students):
        return "Solver module not found yet!"

# PRO: Shtojme meta-data per projektin
app = FastAPI(
    title="AUTS Logic Engine",
    description="API zyrtare për menaxhimin e kapaciteteve në projektin AUTS",
    version="1.1.0"
)

# PRO: Lejojme komunikimin me aplikacione tjera (React/Vue/Mobile)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Lejon çdo pajisje me thirr API-ne
    allow_methods=["*"],
    allow_headers=["*"],
)

class RoomRequest(BaseModel):
    room_name: str = Field(..., example="Dhoma 406")
    # PRO: Sigurohemi qe kapaciteti nuk eshte nen 1
    capacity: int = Field(..., gt=0, description="Kapaciteti duhet te jete numer pozitiv")
    num_students: int = Field(..., ge=0)

@app.get("/", tags=["Health Check"]) # PRO: Tags per dokumentim me te paster
def home():
    return {"status": "Online", "message": "AUTS Logic Engine is ready"}

@app.post("/solve", tags=["Logic"])
def generate_schedule(request: RoomRequest):
    # Logjika e njejte, por tash vjen nga te dhenat e verifikuara
    result = solve_schedule(request.capacity, request.num_students)

    if result == "INFEASIBLE":
        raise HTTPException(status_code=400, detail="Kapaciteti i dhomës është i pamjaftueshëm!")
    
    return {
        "status": "Success",
        "room": request.room_name,
        "message": result
    }