from sqlalchemy import Integer, String, Column, ForeignKey, create_engine, Date, func
from sqlalchemy.orm import Session, declarative_base
from fastapi import HTTPException
from datetime import date, datetime, timedelta, timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

DB_PATH = "blooddrive.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

ph = PasswordHasher()

USERNAME = "sup"
PASSWORD = "12345"
ACCESS_TOKEN_EXPIRY = 15
REFRESH_TOKEN_EXPIRY = 7 * 24 * 60
SECRET_KEY = "secret1234"
ALGORITHM = "HS256"


class Donor(Base):
    __tablename__ = "donors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    roll_no = Column(String, unique=True)
    blood_group = Column(String)
    weight_kg = Column(Integer)
    last_donated_on = Column(Date)


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    donor_id = Column(Integer, ForeignKey("donors.id"))
    drive_date = Column(Date)
    slot = Column(String)
    status = Column(String, default="booked")
    booked_on = Column(Date, default=func.current_date())


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True)
    password = Column(String)
    user_type = Column(String, default="staff")


Base.metadata.create_all(engine)


def seed_data():
    session = Session(engine)
    today = date.today()

    if session.query(Donor).count() == 0:
        donor_records = [
            Donor(id=1, roll_no="AU101", name="Aarav", blood_group="A+", weight_kg=68, last_donated_on=None),
            Donor(id=2, roll_no="AU102", name="Diya", blood_group="O+", weight_kg=55, last_donated_on=today - timedelta(days=30)),
            Donor(id=3, roll_no="AU103", name="Rucha", blood_group="B+", weight_kg=72, last_donated_on=None),
            Donor(id=4, roll_no="AU104", name="Ananya", blood_group="AB+", weight_kg=58, last_donated_on=None),
            Donor(id=5, roll_no="AU105", name="Karthik", blood_group="O-", weight_kg=80, last_donated_on=today - timedelta(days=120)),
            Donor(id=6, roll_no="AU106", name="Sneha", blood_group="A-", weight_kg=52, last_donated_on=today - timedelta(days=45)),
            Donor(id=7, roll_no="AU107", name="Vikram", blood_group="B-", weight_kg=75, last_donated_on=None),
            Donor(id=8, roll_no="AU108", name="Meera", blood_group="O+", weight_kg=60, last_donated_on=today - timedelta(days=200)),
            Donor(id=9, roll_no="AU109", name="Arjun", blood_group="AB-", weight_kg=70, last_donated_on=None),
            Donor(id=10, roll_no="AU110", name="Pooja", blood_group="A+", weight_kg=54, last_donated_on=today - timedelta(days=60)),
            Donor(id=11, roll_no="AU111", name="Viju", blood_group="B+", weight_kg=85, last_donated_on=None),
            Donor(id=12, roll_no="AU112", name="Lakshmi", blood_group="O+", weight_kg=57, last_donated_on=None),
        ]
        session.add_all(donor_records)
        session.commit()

    if session.query(Appointment).count() == 0:
        appointment_records = [
            Appointment(id=1, donor_id=2, drive_date=today - timedelta(days=30), slot="morning", status="donated", booked_on=today - timedelta(days=40)),
            Appointment(id=2, donor_id=6, drive_date=today - timedelta(days=45), slot="afternoon", status="donated", booked_on=today - timedelta(days=55)),
            Appointment(id=3, donor_id=10, drive_date=today - timedelta(days=60), slot="morning", status="donated", booked_on=today - timedelta(days=70)),
            Appointment(id=4, donor_id=5, drive_date=today - timedelta(days=120), slot="morning", status="donated", booked_on=today - timedelta(days=130)),
            Appointment(id=5, donor_id=8, drive_date=today - timedelta(days=200), slot="afternoon", status="donated", booked_on=today - timedelta(days=210)),
            Appointment(id=6, donor_id=11, drive_date=today - timedelta(days=30), slot="afternoon", status="no_show", booked_on=today - timedelta(days=40)),
            Appointment(id=7, donor_id=1, drive_date=today, slot="morning", status="booked", booked_on=today - timedelta(days=3)),
            Appointment(id=8, donor_id=3, drive_date=today + timedelta(days=7), slot="morning", status="booked", booked_on=today),
            Appointment(id=9, donor_id=4, drive_date=today + timedelta(days=7), slot="afternoon", status="booked", booked_on=today),
            Appointment(id=10, donor_id=9, drive_date=today + timedelta(days=14), slot="morning", status="cancelled", booked_on=today),
        ]
        session.add_all(appointment_records)
        session.commit()
    session.close()

seed_data()


def create_token(username, token_type, user_type="staff"):
    time = ACCESS_TOKEN_EXPIRY
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload = {
        "username": username,
        "token_type": token_type,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=time),
        "user_type": user_type,
    }
    return jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token, token_type):
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        return False
    if payload.get("token_type") == token_type:
        return payload["username"]
    return False

def get_user_role(token):
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        if payload["token_type"] != "access":
            return False
        return payload["user_type"]
    except Exception:
        return False

def get_user_type(username):
    session = Session(engine)
    user = session.query(User).filter_by(user_name=username).first()
    user_type = user.user_type if user else None
    session.close()
    return user_type

def register_user(user_name, password, user_type="staff"):
    session = Session(engine)
    if session.query(User).filter_by(user_name=user_name).first() is not None:
        session.close()
        return False
    session.add(User(user_name=user_name, password=ph.hash(password), user_type=user_type))
    session.commit()
    session.close()
    return True

def verify_login(username, password):
    session = Session(engine)
    user = session.query(User).filter_by(user_name=username).first()
    if user is None:
        session.close()
        return False
    try:
        ph.verify(user.password, password)
    except VerifyMismatchError:
        session.close()
        return False
    user_type = user.user_type
    session.close()
    access_token = create_token(username=username, token_type="access", user_type=user_type)
    refresh_token = create_token(username=username, token_type="refresh", user_type=user_type)
    return {"access_token": access_token, "refresh_token": refresh_token}

def get_all_donors(blood_group=None):
    session = Session(engine)
    if blood_group is not None:
        blood_group = blood_group.upper()
        if blood_group not in GROUPS:
            session.close()
            raise HTTPException(status_code=422, detail="Invalid blood group.")
        donors = session.query(Donor).filter(Donor.blood_group == blood_group).all()
    else:
        donors = session.query(Donor).all()

    response = []
    for donor in donors:
        apoint = session.query(Appointment).filter(Appointment.donor_id == donor.id).first()
        if apoint is None:
            status = None
            drive_date = None
        else:
            status = apoint.status
            drive_date = apoint.drive_date
        response.append({
            "id": donor.id,
            "roll_no": donor.roll_no,
            "name": donor.name,
            "blood_group": donor.blood_group,
            "weight_kg": donor.weight_kg,
            "last_donated_on": donor.last_donated_on,
            "status": status,
            "drive_date": drive_date,
        })
    session.close()
    return response

def get_donor(roll_no):
    session = Session(engine)
    donor = session.query(Donor).filter(Donor.roll_no == roll_no).first()
    if donor is None:
        session.close()
        raise HTTPException(status_code=404, detail="Donor not found")

    appoints = session.query(Appointment).filter(Appointment.donor_id == donor.id).all()
    appoint_list = []
    for apoint in appoints:
        appoint_list.append({
            "id": apoint.id,
            "drive_date": apoint.drive_date,
            "slot": apoint.slot,
            "status": apoint.status,
            "booked_on": apoint.booked_on,
        })
    response = {
        "id": donor.id,
        "roll_no": donor.roll_no,
        "name": donor.name,
        "blood_group": donor.blood_group,
        "weight_kg": donor.weight_kg,
        "last_donated_on": donor.last_donated_on,
        "appointments": appoint_list,
    }
    session.close()
    return response


def add_donor(roll_no, name, blood_group, weight_kg):
    roll_no = roll_no.upper()
    blood_group = blood_group.upper()
    if roll_no == "":
        raise HTTPException(status_code=422, detail="Roll number is required.")
    if blood_group not in GROUPS:
        raise HTTPException(status_code=422, detail="Invalid blood group.")
    if weight_kg < 50 or weight_kg > 200:
        raise HTTPException(status_code=422, detail="Weight must be between 50kg and 200kg.")
    session = Session(engine)
    donorexi = session.query(Donor).filter(Donor.roll_no == roll_no).first()
    if donorexi is not None:
        session.close()
        raise HTTPException(status_code=400, detail="Roll number already registered.")

    donor = Donor(roll_no=roll_no, name=name, blood_group=blood_group, weight_kg=weight_kg)
    session.add(donor)
    session.commit()

    response = {
        "id": donor.id,
        "roll_no": donor.roll_no,
        "name": donor.name,
        "blood_group": donor.blood_group,
        "weight_kg": donor.weight_kg,
        "last_donated_on": donor.last_donated_on,
    }
    session.close()
    return response

def get_eligible_donors(blood_group):
    blood_group = blood_group.upper()
    if blood_group not in GROUPS:
        raise HTTPException(status_code=422, detail="Blood group must be A+ , B+ ,O+ ,AB+ ,A- ,B- ,O- ,AB-")
    session = Session(engine)
    donors = session.query(Donor).filter(Donor.blood_group == blood_group).all()
    response = []
    for donor in donors:
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
                "last_donated_on": donor.last_donated_on,
            })
    session.close()
    return response

def book_appoint(roll_no, drive_date, slot):
    if slot not in ["morning", "afternoon"]:
        raise HTTPException(status_code=422, detail="Invalid Slot")
    try:
        drive_date = datetime.strptime(drive_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=422, detail="Date must be written as YYYY-MM-DD")
    if drive_date < datetime.now().date():
        raise HTTPException(status_code=400, detail="Drive date cannot be past")
    session = Session(engine)
    donor = session.query(Donor).filter(Donor.roll_no == roll_no).first()
    if donor is None:
        session.close()
        raise HTTPException(status_code=404, detail="Donor not found")
    if donor.last_donated_on is not None:
        next_donation = donor.last_donated_on + timedelta(days=90)
        if drive_date < next_donation:
            session.close()
            raise HTTPException(status_code=400, detail=f"You can donate again from {next_donation}.")
    appoint = session.query(Appointment).filter(
        Appointment.donor_id == donor.id, Appointment.status == "booked").first()
    if appoint is not None:
        session.close()
        raise HTTPException(status_code=400, detail="You already have a booked appointment")
    count = session.query(Appointment).filter(
        Appointment.drive_date == drive_date,
        Appointment.slot == slot,
        Appointment.status == "booked").count()
    if count >= 10:
        session.close()
        raise HTTPException(status_code=400, detail="Slot Full")
    apoint = Appointment(
        donor_id=donor.id,
        drive_date=drive_date,
        slot=slot,
        status="booked",
        booked_on=date.today(),
    )
    session.add(apoint)
    session.commit()
    response = {
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
    return response

def cancel_appoint(id):
    session = Session(engine)
    apoint = session.get(Appointment, id)
    if apoint is None:
        session.close()
        raise HTTPException(status_code=404, detail="Appointment not found")
    if apoint.status != "booked":
        session.close()
        raise HTTPException(status_code=400, detail="Appointment cannot be cancelled")
    apoint.status = "cancelled"
    session.commit()
    donor = session.get(Donor, apoint.donor_id)
    response = {
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
    return response

def mark_appoint(id, status):
    if status not in ["donated", "no_show"]:
        raise HTTPException(status_code=422, detail="Invalid Status")
    session = Session(engine)
    apoint = session.get(Appointment, id)
    if apoint is None:
        session.close()
        raise HTTPException(status_code=404, detail="Appointment not found")
    if apoint.status != "booked":
        session.close()
        raise HTTPException(status_code=400, detail=f"Appointment cannot be marked, current status is {apoint.status}")
    if apoint.drive_date > datetime.now().date():
        session.close()
        raise HTTPException(status_code=400, detail=f"Appointment cannot be marked, drive date is in future {apoint.drive_date}")
    apoint.status = status
    donor = session.get(Donor, apoint.donor_id)
    if status == "donated":
        donor.last_donated_on = apoint.drive_date
    session.commit()
    response = {
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
    return response

def get_appointments_by_date(drive_date):
    if len(drive_date) != 10 or drive_date[4] != "-" or drive_date[7] != "-":
        raise HTTPException(status_code=422, detail="Date must be written as YYYY-MM-DD")
    try:
        drive_date = datetime.strptime(drive_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=422, detail="Date must be written as YYYY-MM-DD")
    session = Session(engine)
    response = []
    for slot in ["morning", "afternoon"]:
        apointsday = session.query(Appointment).filter(
            Appointment.drive_date == drive_date,
            Appointment.slot == slot).all()
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
    donated = session.query(Appointment).filter(Appointment.status == "donated").all()
    for donate in donated:
        donor = session.get(Donor, donate.donor_id)
        unitscounts[donor.blood_group] += 1
    session.close()
    return unitscounts