from sqlalchemy import Integer, String, Column, create_engine, Date, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import date

DB_PATH = "warehouse5.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Packages(Base):
    __tablename__ = "packages"
    id = Column(Integer, primary_key=True)
    package_name = Column(String)
    destination = Column(String)
    weight = Column(Integer)
    arrival_date = Column(Date)
    status = Column(String)


class Dispatch(Base):
    __tablename__ = "dispatch"
    id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey("packages.id"))
    vehicle = Column(String)
    destination = Column(String)
    dispatch_status = Column(String)
    man_date = Column(Date)


Base.metadata.create_all(engine)


def register_package(package_name,destination,weight,arrival_date,status):
    session = Session(engine)
    package = Packages(package_name=package_name,destination=destination,weight=weight,arrival_date=date.today(),status=status)
    session.add(package)
    session.commit()
    response = {
        "id": package.id,
        "package_name": package.package_name,
        "destination":package.destination,
        "weight":package.weight,
        "arrival_date":package.arrival_date,
        "status":package.status
    }
    session.close()
    return response



def get_details(package_id):
    session = Session(engine)
    package = session.get(Packages,package_id)
    if package is None:
        session.close()
        return None
    response ={
        "id": package.id,
        "package_name": package.package_name,
        "destination":package.destination,
        "weight":package.weight,
        "arrival_date":package.arrival_date,
        "status":package.status
    }
    session.close()
    return response



def update_package(package_id,destination,status):
    session = Session(engine)
    package =  session.get(Packages,package_id)
    if package is None:
        session.close()
        return None
    if destination is not None:
        package.destination = destination
    if status is not None:
        package.destination = status
    session.commit()
    response = {
        "id": package.id,
        "package_name": package.package_name,
        "destination":package.destination,
        "weight":package.weight,
        "arrival_date":package.arrival_date,
        "status":package.status
    }
    session.close()
    return response



# def delete_package(package_id):
#     session = Session(engine)
#     package = session.get(Packages,package_id)
#     session.delete(package)
#     session.commit()
#     session.close()


# def search_packages(destination,status,arrival_date):
#     session = Session(engine)
#     packages = session.query(Packages).all()
#     response = []
#     for package in packages:
#         if destination and package.destination is not destination:




