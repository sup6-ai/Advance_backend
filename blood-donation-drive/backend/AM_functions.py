from sqlalchemy import Integer, String, Column, ForeignKey, create_engine,Date,func
from sqlalchemy.orm import Session, declarative_base
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from datetime import date,datetime,timedelta

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
            Appointment(id=6,  donor_id=11, drive_date=today - timedelta(days=30),  slot="afternoon", status="booked", booked_on=today),
            Appointment(id=7,  donor_id=1,  drive_date=today,                       slot="morning",   status="booked",  booked_on=today - timedelta(days=3)),
            Appointment(id=8,  donor_id=3,  drive_date=today + timedelta(days=7),   slot="morning",   status="booked",  booked_on=today),
            Appointment(id=9,  donor_id=4,  drive_date=today,                       slot="afternoon", status="booked",  booked_on=today),
            Appointment(id=10, donor_id=9,  drive_date=today + timedelta(days=14),  slot="morning",   status="cancelled", booked_on=today),
        ]
        session.add_all(appointment_records)
        session.commit()
    session.close()



seed_data()


def book_appoint(roll_no,drive_date,slot):
    drive_date = datetime.strptime(drive_date, "%Y-%m-%d").date()

    session=Session(engine)
    
    if slot not in ["morning","afternoon"]:
        raise HTTPException(status_code = 422,detail="Invalid Slot")

    if drive_date < datetime.now().date():
        session.close()
        raise HTTPException(status_code = 400,detail="Drive date cannot be past")



    donor = session.query(Donor).filter(Donor.roll_no == roll_no).first()
    if donor is None:
       session.close()
       raise HTTPException(status_code=404, detail="Donor not found")
    
    if donor.last_donated_on is not None:
        next_donation = donor.last_donated_on + timedelta(days=90)
        if drive_date < next_donation:
            session.close()
            raise HTTPException(status_code=400, detail=f"You can donate again from {next_donation}.")

    appoint = session.query(Appointment).filter(Appointment.donor_id == donor.id,Appointment.status =="booked").first()
    if appoint is not None:
        session.close()
        raise HTTPException(status_code = 400,detail ="You alreday have a booked appoinmtent")

    count = session.query(Appointment).filter(Appointment.drive_date == drive_date,Appointment.slot == slot,Appointment.status=="booked").count()
    if count >= 10:
        session.close()
        raise HTTPException(status_code = 400,detail="Slot Full")


    apoint=Appointment(
        donor_id=donor.id,
        drive_date=drive_date,
        slot=slot,
        status="booked",
        booked_on=func.current_date()
        )
    session.add(apoint)
    session.commit()
    responce={
        "id": apoint.id,
        "donor_id": donor.id,
        "roll_no": donor.roll_no,
        "name": donor.name,
        "blood_group": donor.blood_group,
        "drive_date": apoint.drive_date,
        "slot": apoint.slot,
        "status": apoint.status,
        "booked_on": apoint.booked_on,
    }
    session.close()
    return responce
       
def cancel_appoint(id):
    session=Session(engine)
    apoint = session.get(Appointment,id)

    if apoint is None:
        session.close()
        raise HTTPException(status_code = 404,detail="Appointment not found")

    if apoint.status!= "booked":
        session.close()
        raise HTTPException(status_code = 400,detail="Appointment cannot be cancelled")

    apoint.status = "cancelled"
    session.commit()
    donor = session.get(Donor, apoint.donor_id)
    responce = {
        "id": apoint.id,
        "donor_id": apoint.donor_id,
        "roll_no": donor.roll_no,
        "name": donor.name,
        "drive_date": apoint.drive_date,
        "slot": apoint.slot,
        "status": apoint.status,
        "booked_on": apoint.booked_on,
    }
    session.close()
    return responce


def mark_appoint(id,status):
    session=Session(engine)
    if status not in ["donated","no_show"]:
        session.close()
        raise HTTPException(status_code = 422,detail="Invalid Status")  

    apoint = session.get(Appointment,id)

    if apoint is None:
        session.close()
        raise HTTPException(status_code = 404,detail="Appointment not found")

    if apoint.status != "booked":
        session.close()
        raise HTTPException(status_code = 400,detail=f"Appointment cannot be marked status {apoint.status}")

    
    if apoint.drive_date > datetime.now().date():
        session.close()
        raise HTTPException(status_code = 400,detail=f"Appointment cannot be marked drive date in future {apoint.drive_date}")

    apoint.status = status
    donor = session.get(Donor, apoint.donor_id)
    if status == "donated":
        donor.last_donated_on = apoint.drive_date
        
    session.commit()
    responce = {
        "id": apoint.id,
        "donor_id": apoint.donor_id,
        "roll_no": donor.roll_no,
        "name": donor.name,
        "drive_date": apoint.drive_date,
        "slot": apoint.slot,
        "status": apoint.status,
        "booked_on": apoint.booked_on,
    }
    session.close()
    return responce
