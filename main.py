from ortools.sat.python import cp_model

def solve_room_capacity():
    # 1. Krijimi i modelit (Truri i AI)
    model = cp_model.CpModel()

    # 2. Të dhënat (Slice 1: Fokus te Kapaciteti i Dhomave)
    room_capacity = 25  # Psh. Dhoma 406
    num_students = 10   # Një vlerë testuese

    # 3. Poka-Yoke Constraint: Matematika që nuk lejon gabime
    # Ne po i themi AI: num_students duhet të jetë <= room_capacity
    is_valid = num_students <= room_capacity

    if is_valid:
        return "Orari është në rregull: Kapaciteti mjafton."
    else:
        return "GABIM: Dhoma nuk ka vend për kaq shumë studentë!"

print(solve_room_capacity())