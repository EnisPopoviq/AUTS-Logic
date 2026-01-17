from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Marrim funksioninin nga partnerja
try:
    from solver import solve_schedule 
except ImportError:
    # Nese ajo s'e ka kry punen, krijojme nje version "fake" (mock)
    def solve_schedule(capacity, students):
        return "Solver module not found yet!"

# --- PREJ KETU, KODI DUHET TE JETE NE FILLIM TE RRESHTIT ---

# Krijojme objektin kryesor te aplikacionit
app = FastAPI(title="AUTS Logic Engine", version="1.0")

# Definojme modelin e te dhenave (Pydantic)
class RoomRequest(BaseModel):
    room_name: str
    capacity: int
    num_students: int

# Faqja kryesore (Home)
@app.get("/")
def home():
    return {"status": "Online", "message": "AUTS Logic Engine is ready"}

# Pika ku kryhet puna (Endpoint)
@app.post("/solve")
def generate_schedule(request: RoomRequest):
    # Therrasim logjiken
    result = solve_schedule(request.capacity, request.num_students)

    # Menaxhojme rastin kur nuk ka zgjidhje
    if result == "INFEASIBLE":
        raise HTTPException(status_code=400, detail="No feasible schedule found!")
    
    # Kthejme pergjigjen finale
    return {
        "status": "Success",
        "room": request.room_name,
        "message": result
    }