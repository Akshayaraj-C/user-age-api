# Python FastAPI User Age API

A high-performance backend RESTful API built in Python using **FastAPI**, **SQLModel**, and asynchronous **PostgreSQL** (`asyncpg`). This application supports public user CRUD operations and dynamically calculates the user's age on serialization.

---

## 🔧 Tech Stack

* **Language**: Python 3.10+
* **Web Framework**: [FastAPI](https://fastapi.tiangolo.com/)
* **API Documentation**: [Scalar API Docs](https://github.com/scalar/scalar) (Served at `/scalar`)
* **ORM & Database Access**: [SQLModel](https://sqlmodel.tiangolo.com/) with asynchronous PostgreSQL support (`asyncpg`)
* **Testing**: [Pytest](https://pytest.org/)

---

## 🚀 Key Features

* **Public User CRUD Endpoints**: Create, Read, Update, and Delete users without login or session restrictions.
* **Flexible DOB Parsing & Validation**: Supports multiple input formats for the Date of Birth (`dob`):
  * `YYYY-MM-DD`
  * `DD/MM/YYYY`
  * `DD-MM-YYYY`
* **Dynamic Age Calculation**: Age is calculated on-the-fly when serialization occurs using Python's `datetime` package inside a Pydantic `@computed_field`. It is **never** stored in the database.
* **Request Logger Middleware**: Logs incoming requests, latency, and propagates a unique request ID using custom ASGI middleware.
* **Auto-Schema Creation**: Relies on SQLModel to compile schemas and automatically initialize tables on startup inside FastAPI's `lifespan` handler.

---

## 🏃 Running the Application

### 1. Prerequisites
* **Python 3.10+** installed.
* **PostgreSQL** running locally.

### 2. Configure Environment Variables
Create a `.env` file in the project root:
```env
APP_NAME="User Age API"
DEBUG=true

# Database Configuration
DB_HOST=127.0.0.1
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgresql
DB_NAME=user_age_db
```

### 3. Install Dependencies
Create a virtual environment and install project packages:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the Server
Start the Uvicorn web server:
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8081 --reload
```

* The API server will begin running on [http://localhost:8081](http://localhost:8081).
* You can access the interactive Scalar API documentation at: **`http://localhost:8081/scalar`**

---

## 🧪 Running Unit Tests

To verify the service and age calculation logic, run:

```bash
pytest
```

---

## 📊 API Testing Examples

You can use the **Scalar Docs** page at `http://localhost:8081/scalar` or use standard HTTP clients:

### 1. Create a User
**POST** `/users/`
```bash
curl -i -X POST http://localhost:8081/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Akshayaraj C", "dob": "30/06/2004"}'
```

*Response:*
```json
{
  "id": 1,
  "name": "Akshayaraj C",
  "dob": "2004-06-30",
  "age": 21
}
```

### 2. Get All Users (with Pagination)
**GET** `/users/?page=1&limit=10`
```bash
curl -i http://localhost:8081/users/
```

### 3. Get User By ID
**GET** `/users/1`
```bash
curl -i http://localhost:8081/users/1
```

### 4. Update a User
**PATCH** `/users/1`
```bash
curl -i -X PATCH http://localhost:8081/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Akshayaraj"}'
```

### 5. Delete a User
**DELETE** `/users/1`
```bash
curl -i -X DELETE http://localhost:8081/users/1
```
