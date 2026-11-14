from fastapi import FastAPI, HTTPException, Header, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import functions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USER_TYPE = ["admin", "staff"]

def check_role(token, allowed_roles):
    username = functions.verify_token(token=token, token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_type = functions.get_user_role(token)
    if user_type not in allowed_roles:
        raise HTTPException(status_code=403, detail="Permission denied")

class DonorDetails(BaseModel):
    roll_no: str = Field(min_length=1)
    name: str = Field(min_length=1)
    blood_group: str
    weight_kg: int = Field(ge=50, le=200)

class AppointmentDetails(BaseModel):
    roll_no: str = Field(min_length=1)
    drive_date: str
    slot: str

class StatusUpdate(BaseModel):
    status: str

class UserRegister(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=8)
    user_type: str

@app.post("/login")
def login(username=Body(), password=Body()):
    token = functions.verify_login(username=username, password=password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return token

@app.post("/refresh")
def refresh(refresh_token=Header(None)):
    username = functions.verify_token(token=refresh_token, token_type="refresh")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    user_type = functions.get_user_type(username)
    if user_type is None:
        raise HTTPException(status_code=401, detail="User no longer exists")
    access_token = functions.create_token(username=username, token_type="access", user_type=user_type)
    return {"access_token": access_token}

@app.post("/register_user")
def register_user(user: UserRegister):
    if user.user_type not in USER_TYPE:
        raise HTTPException(status_code=400, detail="user_type must be admin or staff")
    if functions.register_user(user_name=user.username, password=user.password, user_type=user.user_type):
        return {"message": "user registered successfully"}
    raise HTTPException(status_code=400, detail="user already exists")

@app.get("/donors")
def donors(blood_group=None, token=Header(None)):
    check_role(token, ["admin", "staff"])
    return functions.get_all_donors(blood_group=blood_group)

@app.get("/donors/eligible")
def get_eligible_donors(blood_group, token=Header(None)):
    check_role(token, ["admin", "staff"])
    return functions.get_eligible_donors(blood_group)

@app.get("/donors/{roll_no}")
def get_donor(roll_no: str, token=Header(None)):
    check_role(token, ["admin", "staff"])
    return functions.get_donor(roll_no.upper())

@app.post("/donors")
def add_donor(donor: DonorDetails, token=Header(None)):
    check_role(token, ["admin"])
    return functions.add_donor(
        roll_no=donor.roll_no,
        name=donor.name,
        blood_group=donor.blood_group,
        weight_kg=donor.weight_kg)

@app.post("/appointments")
def book_appoint(appointment: AppointmentDetails, token=Header(None)):
    check_role(token, ["admin", "staff"])
    return functions.book_appoint(
        appointment.roll_no.upper(),
        appointment.drive_date,
        appointment.slot.lower())

@app.patch("/appointments/{id}/cancel")
def cancel_appoint(id: int, token=Header(None)):
    check_role(token, ["admin"])
    return functions.cancel_appoint(id)

@app.patch("/appointments/{id}/status")
def mark_appoint(id: int, data: StatusUpdate, token=Header(None)):
    check_role(token, ["admin"])
    return functions.mark_appoint(id, data.status.lower())

@app.get("/appointments")
def get_appointments(drive_date, token=Header(None)):
    check_role(token, ["admin", "staff"])
    return functions.get_appointments_by_date(drive_date)

@app.get("/appointments/status/units")
def get_units(token=Header(None)):
    check_role(token, ["admin"])
    return functions.get_units()