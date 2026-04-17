# Leave Management API

A lightweight, high-performance RESTful API for managing employee leave requests, balances, and employee records using **FastAPI** and **JSON flat-file storage**.

## Features

* Employee Management
* Leave Request Submission
* Automatic Leave Day Calculation
* Leave Balance Validation
* JSON File Database
* Thread-Safe Read/Write Operations
* Swagger API Documentation
* OpenAPI JSON Support

---

## Tech Stack

* Python 3.10+
* FastAPI
* Uvicorn
* FileLock
* Pydantic

---

## Project Structure

```bash
leave-management-api/
│── main.py
│── database.json
│── requirements.txt
│── README.md
```

---

## Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/leave-management-api.git
cd leave-management-api
```

### 2. Create Virtual Environment (Recommended)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Project

```bash
uvicorn main:app --reload
```

Server will start at:

```bash
http://127.0.0.1:8000
```

---

## API Documentation

### Swagger UI

```bash
http://127.0.0.1:8000/docs
```

### OpenAPI JSON

```bash
http://127.0.0.1:8000/openapi.json
```

---

## API Endpoints

## Employees

| Method | Endpoint       |
| ------ | -------------- |
| GET    | /api/employees |
| POST   | /api/employees |

---

## Leaves

| Method | Endpoint                  |
| ------ | ------------------------- |
| GET    | /api/leaves/employee/{id} |
| POST   | /api/leaves               |

---

## Leave Balances

| Method | Endpoint                                     |
| ------ | -------------------------------------------- |
| GET    | /api/leavebalances/employee/{id}/year/{year} |

---

## Sample Request

### Add Employee

```json
POST /api/employees

{
  "firstName": "Dipsekhar",
  "lastName": "Maity",
  "email": "dip@gmail.com",
  "department": "IT",
  "joinDate": "2026-04-17"
}
```

---

### Apply Leave

```json
POST /api/leaves

{
  "employeeId": 1,
  "startDate": "2026-04-20",
  "endDate": "2026-04-22",
  "leaveType": "Annual",
  "reason": "Vacation"
}
```

---

## Response Format

```json
{
  "success": true,
  "message": "Detailed action message",
  "data": {}
}
```

---

## Run in Postman

1. Open Postman
2. Import endpoints manually
3. Use Base URL:

```bash
http://127.0.0.1:8000
```

---

## Deployment

You can deploy this project on:

* Render
* Railway
* PythonAnywhere

---

## Author

Dipsekhar Maity

---
