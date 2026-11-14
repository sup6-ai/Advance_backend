from sqlalchemy import Integer, String, Column, ForeignKey, create_engine,Date,func
from sqlalchemy.orm import Session, declarative_base
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import date,timedelta,datetime
GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

DB_PATH = "blooddrive.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Donor(Base):
    __tablename__="donors"
    id = Column(Integer,primary_key = True)
    name = Column(String)
    roll_no = Column(String,unique = True)
    blood_group = Column(String)
    weight_kg = Column(Integer)
    last_donated_on = Column(Date)
     
class Appointment(Base):
    __tablename__="appointments"   
    id = Column(Integer,primary_key = True)
    donor_id = Column(Integer, ForeignKey("donors.id"))
    drive_date = Column(Date)
    slot = Column(String)
    status = Column(String,default = "booked")
    booked_on = Column(Date,default = func.current_date())   
Base.metadata.create_all(engine)

def seed_data():
    session = Session(engine)
    today = date.today()
    if session.query(Donor).count() == 0:
        donor_records = [
            Donor(id=1,roll_no="AU101", name="Aarav",blood_group="A+",weight_kg=68,last_donated_on=None),
            Donor(id=2, roll_no="AU102", name="Diya",blood_group="O+",weight_kg=55,last_donated_on=today - timedelta(days=30)),   
            Donor(id=3,roll_no="AU103", name="Rucha",blood_group="B+",weight_kg=72,last_donated_on=None),
            Donor(id=4,roll_no="AU104", name="Ananya",blood_group="AB+", weight_kg=58, last_donated_on=None),
            Donor(id=5,roll_no="AU105", name="Karthik",blood_group="O-",weight_kg=80, last_donated_on=today - timedelta(days=120)),  
            Donor(id=6,roll_no="AU106", name="Sneha",blood_group="A-",  weight_kg=52,last_donated_on=today - timedelta(days=45)),   
            Donor(id=7,roll_no="AU107", name="Vikram",blood_group="B-",weight_kg=75, last_donated_on=None),
            Donor(id=8,roll_no="AU108", name="Meera",blood_group="O+", weight_kg=60, last_donated_on=today - timedelta(days=200)),  
            Donor(id=9,roll_no="AU109", name="Arjun",blood_group="AB-",weight_kg=70, last_donated_on=None),
            Donor(id=10,roll_no="AU110", name="Pooja",blood_group="A+", weight_kg=54, last_donated_on=today - timedelta(days=60)),   
            Donor(id=11,roll_no="AU111", name="Viju",blood_group="B+", weight_kg=85, last_donated_on=None),
            Donor(id=12,roll_no="AU112",name="Lakshmi",blood_group="O+",  weight_kg=57, last_donated_on=None),
        ]
        session.add_all(donor_records)
        session.commit()

    if session.query(Appointment).count() == 0:
        appointment_records = [         
            Appointment(id=1,  donor_id=2,  drive_date=today - timedelta(days=30),  slot="morning",   status="donated", booked_on=today - timedelta(days=40)),
            Appointment(id=2,  donor_id=6,  drive_date=today - timedelta(days=45),  slot="afternoon", status="donated", booked_on=today - timedelta(days=55)),
            Appointment(id=3,  donor_id=10, drive_date=today - timedelta(days=60),  slot="morning",   status="donated", booked_on=today - timedelta(days=70)),
            Appointment(id=4,  donor_id=5,  drive_date=today - timedelta(days=120), slot="morning",   status="donated", booked_on=today - timedelta(days=130)),
            Appointment(id=5,  donor_id=8,  drive_date=today - timedelta(days=200), slot="afternoon", status="donated", booked_on=today - timedelta(days=210)),
            Appointment(id=6,  donor_id=11, drive_date=today - timedelta(days=30),  slot="afternoon", status="no_show", booked_on=today - timedelta(days=40)),
            Appointment(id=7,  donor_id=1,  drive_date=today,                       slot="morning",   status="booked",  booked_on=today - timedelta(days=3)),
            Appointment(id=8,  donor_id=3,  drive_date=today + timedelta(days=7),   slot="morning",   status="booked",  booked_on=today),
            Appointment(id=9,  donor_id=4,  drive_date=today + timedelta(days=7),   slot="afternoon", status="booked",  booked_on=today),
            Appointment(id=10, donor_id=9,  drive_date=today + timedelta(days=14),  slot="morning",   status="cancelled", booked_on=today),
        ]
        session.add_all(appointment_records)
        session.commit()
    session.close()
seed_data()

def get_appointments_by_date(drive_date):
    if len(drive_date) != 10 or drive_date[4] != "-" or drive_date[7] != "-":
            raise HTTPException(status_code=422, detail="Date must be written as YYYY-MM-DD")
    drive_date = datetime.strptime(drive_date, "%Y-%m-%d").date()
    session = Session(engine)
    response = []

    for slot in ["morning", "afternoon"]:
        apointsday = session.query(Appointment).filter(
            Appointment.drive_date == drive_date,
            Appointment.slot == slot
        ).all()

        for apoint in apointsday:
            donor = session.get(Donor, apoint.donor_id)
            response.append({
                "id": apoint.id,
                "donor_id": donor.id,
                "name": donor.name,
                "blood_group": donor.blood_group,
                "drive_date": apoint.drive_date,
                "slot": apoint.slot,
                "status": apoint.status,
            })

    session.close()
    return response

def get_units():                                           
    session = Session(engine)
    unitscounts = {}
    for g in GROUPS:
        unitscounts[g] = 0
    donated = session.query(Appointment).filter(Appointment.status=="donated").all()
    for donate in donated:                                   
        donor = session.get(Donor , donate.donor_id)   
        unitscounts[donor.blood_group] +=1
    session.close()
    return unitscounts

def get_eligible_donors(blood_group): 
    blood_group=blood_group.upper() 
    if blood_group not in GROUPS:
            raise HTTPException(status_code=422 , detail="Blood group must be A+ , B+ ,O+ ,AB+ ,A- ,B- ,O- ,AB-")                    
    session = Session(engine)
    donors = session.query(Donor).filter(Donor.blood_group == blood_group).all()
    response = []
    for donor in donors :
        booked = session.query(Appointment).filter(
            Appointment.donor_id == donor.id,
            Appointment.status == "booked").first()      
        eligible_day = datetime.now().date()                         
        if donor.last_donated_on is not None:             
            eligible_day = donor.last_donated_on + timedelta(days=90)   
        if eligible_day <= datetime.now().date() and booked is None:   
            response.append({              
                "name": donor.name,
                "roll_no": donor.roll_no,
                "blood_group": donor.blood_group,
                "weight_kg": donor.weight_kg,
                "last_donated_on": donor.last_donated_on})         
    session.close()
    return response
