from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel, Field 
from typing import Optional, Dict, Any

# --- PJESA 1: LIDHJA ME TRURIN (SOLVER) ---
# Ktu pe kqyrum a e ka kry partnerja punen e vet ne 'solver.py'.
# Nese ajo s'e ka kry, na e krijojme ni funksion fallc (mock) sa mos me na u prish serveri.
try:
    from solver import solve_schedule 
except ImportError:
    def solve_schedule(capacity, students):
        return "Solver module not found yet!"

# --- PJESA 2: KONFIGURIMI I SERVERIT ---
# Ktu po e dhezim serverin edhe po i qesim do informata shtese per dokumentacion.
app = FastAPI(
    title="AUTS Logic Engine",
    description="API zyrtare per menaxhimin e kapaciteteve. Ky osht motori i logjikes.",
    version="1.2.0"
)

# --- PJESA 3: HAPJA E DYERVE (CORS) ---
# Kjo pjese osht kritike. Pa kete, React ose Mobile app nuk mujn me fol me neve.
# Na po i thojme "Lejoje krejtve me hi" (allow_origins=["*"]).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- PJESA 4: RREGULLAT E LOJES (DATA MODELS) ---

# Qekjo tregon qysh duhet me na ardh kerkesa prej Oltit (Backend).
class RoomRequest(BaseModel):
    room_name: str = Field(..., example="Dhoma 406", description="Emri i dhomes qe po dojm me testu")
    
    # Ktu po bojm 'Defense'. S'lejojme kapacitet 0 ose negativ.
    capacity: int = Field(..., gt=0, description="Sa studenta nxen dhoma (s'bon me kon 0 ose ma pak)")
    
    # Numri i studentave s'bon me kon negativ.
    num_students: int = Field(..., ge=0, description="Sa studenta kemi planifiku")

# Qekjo tregon qysh kemi me ja kthy pergjigjen. Osht mire per dokumentim.
class RoomResponse(BaseModel):
    status: str
    room: str
    message: str

# --- PJESA 5: ENDPOINTS (BUTONAT E SERVERIT) ---

# 1. Health Check - Sa me kqyr a jemi gjalle.
@app.get("/", tags=["System Check"]) 
def home():
    return {"status": "Online", "message": "AUTS Logic Engine osht dhezun dhe gati."}

# 2. Logjika Kryesore - Ktu ndodh magjia.
@app.post("/solve", response_model=RoomResponse, tags=["Logic"])
def generate_schedule(request: RoomRequest):
    # E marrim kerkesen, i qesim ne terminal sa me pa na qe po punon
    print(f"📥 Erdhi kerkesa per: {request.room_name} | Kapaciteti: {request.capacity}")

    # Ja pasojme topin partneres (funksionit solver)
    result = solve_schedule(request.capacity, request.num_students)

    # Nese solveri thot "S'bohet", na kthejme error 400 (Bad Request)
    if result == "INFEASIBLE":
        raise HTTPException(status_code=400, detail="Nuk ka vend ne dhome per keta studenta!")
    
    # Nese krejt osht ne rregull, ja kthejme pergjigjen pozitive
    return {
        "status": "Success",
        "room": request.room_name,
        "message": result
    }