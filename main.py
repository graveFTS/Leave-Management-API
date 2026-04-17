from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import date
from filelock import FileLock
import json

app = FastAPI(title="Leave Management API")

DB_FILE = "database.json"
LOCK = FileLock("database.lock")


def read_db():
    with LOCK:
        with open(DB_FILE, "r") as f:
            return json.load(f)


def write_db(data):
    with LOCK:
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=2)


def response(success, message, data):
    return {
        "success": success,
        "message": message,
        "data": data
    }


class Employee(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    department: str
    joinDate: date


class LeaveRequest(BaseModel):
    employeeId: int
    startDate: date
    endDate: date
    leaveType: str
    reason: str


# ---------------- Employees ----------------

@app.get("/api/employees")
def get_employees():
    db = read_db()
    return response(True, "Employees fetched", db["employees"])


@app.post("/api/employees")
def add_employee(emp: Employee):
    db = read_db()

    new_id = max([e["employeeId"] for e in db["employees"]], default=0) + 1

    new_emp = emp.dict()
    new_emp["employeeId"] = new_id
    new_emp["joinDate"] = str(new_emp["joinDate"])

    db["employees"].append(new_emp)
    write_db(db)

    return response(True, "Employee added", new_emp)


# ---------------- Leave ----------------

@app.post("/api/leaves")
def apply_leave(req: LeaveRequest):
    db = read_db()

    if req.endDate < req.startDate:
        raise HTTPException(400, "End date must be after start date")

    total_days = (req.endDate - req.startDate).days + 1
    year = req.startDate.year

    balance = next(
        (b for b in db["balances"]
         if b["employeeId"] == req.employeeId
         and b["year"] == year
         and b["leaveType"].lower() == req.leaveType.lower()),
        None
    )

    if not balance:
        raise HTTPException(404, "Balance record not found")

    if balance["days"] < total_days:
        raise HTTPException(400, "Not enough leave balance")

    leave_id = len(db["leaves"]) + 1

    leave = {
        "leaveId": leave_id,
        "employeeId": req.employeeId,
        "startDate": str(req.startDate),
        "endDate": str(req.endDate),
        "leaveType": req.leaveType,
        "reason": req.reason,
        "totalDays": total_days,
        "status": "Pending"
    }

    db["leaves"].append(leave)
    write_db(db)

    return response(True, "Leave applied", leave)


@app.get("/api/leaves/employee/{id}")
def get_employee_leaves(id: int):
    db = read_db()
    data = [l for l in db["leaves"] if l["employeeId"] == id]
    return response(True, "Leaves fetched", data)


# ---------------- Balance ----------------

@app.get("/api/leavebalances/employee/{id}/year/{year}")
def get_balance(id: int, year: int):
    db = read_db()
    data = [b for b in db["balances"] if b["employeeId"] == id and b["year"] == year]
    return response(True, "Balance fetched", data)