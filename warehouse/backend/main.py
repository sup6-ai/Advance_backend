from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["", ""],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/packages")
def register_packages(package_name,destination,weight,arrival_date,status):
    return functions.register_package(package_name=package_name,destination=destination,weight=weight,arrival_date=arrival_date,status=status)


@app.get("/packages/{package_id}")
def get_details(package_id):
    package = functions.get_details(package_id=package_id)
    if package is None:
        raise HTTPException(status_code=404, detail="Not found")
    return package


@app.patch("/packages/{package_id}")
def update_package(package_id, destination=None, status=None):
    if functions.get_details(package_id=package_id) is None:
        raise HTTPException(status_code=404, detail="Not found")
    return functions.update_package(package_id=package_id, destination=destination, status=status)




