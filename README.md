# Python FastAPI User Age API

A high-performance backend RESTful API built in Python using the exact stack from the **FastShip** project: **FastAPI**, **SQLModel**, **PostgreSQL (asyncpg)**, **Redis** (for JWT blacklist tracking), and **Docker**. 

This application supports user registration, login, logout, and protected CRUD operations that calculate the user's age dynamically on serialization.

---

## 🔧 Tech Stack

* **Language**: Python 3.10+
* **Web Framework**: [FastAPI](https://fastapi.tiangolo.com/) 
* **API Documentation**: [Scalar API Docs](https://github.com/scalar/scalar) (Served at `/scalar`)
* **ORM & Database Access**: [SQLModel](https://sqlmodel.tiangolo.com/) with asynchronous PostgreSQL support (`asyncpg`)
* **Authentication**: JWT (JSON Web Tokens via `pyjwt`) and password hashing via `passlib[bcrypt]`
* **Session Cache / Token Blacklist**: [Redis](https://redis.io/)
* **Testing**: [Pytest](https://pytest.org/)
* **Containerization**: [Docker & Docker Compose](https://www.docker.com/)

---

## 🚀 Key Features

* **Authentication (Register/Login/Logout)**:
  * Users can register with their email, name, DOB, and password (`POST /auth/register`).
  * Users can login to retrieve a JWT access token (`POST /auth/login`).
  * Users can logout to blacklist their current token's unique ID (`jti`) in Redis (`POST /auth/logout`).
* **Secured CRUD Operations**: All user management endpoints are protected and require a valid JWT header (`Authorization: Bearer <token>`).
* **Dynamic Age Calculation**: Age is calculated on-the-fly when serialization occurs using Python's `datetime` package inside a Pydantic `@computed_field`. It is **never** stored in the database.
* **Auto-Schema Creation**: Relies on SQLModel to compile schemas and automatically initialize tables on startup inside FastAPI's `lifespan` handler (no Alembic migrations required).
* **Pagination**: Supports pagination of users using query params: `/users?page=1&limit=10`.

---

## 🏃 Running the Application

### Method 1: Running with Docker (Recommended)

To spin up the PostgreSQL database, Redis session cache, and FastAPI server together in one command:

```bash
docker-compose up --build
```

The API server will begin running on [http://localhost:8080](http://localhost:8080).
You can access the interactive Scalar API documentation at: **`http://localhost:8080/scalar`**

### Method 2: Local Setup (Without Docker)

#### 1. Prerequisites
* **Python 3.10+** installed.
* **PostgreSQL** running locally on port `5432` with username/password `postgres/postgres`.
* **Redis** running locally on port `6379`.

#### 2. Install Dependencies
Create a virtual environment and install project packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 3. Run the Server
Start the Uvicorn web server:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
```

---

## 🧪 Running Unit Tests

To verify the age calculation logic, run:

```bash
pytest
```

---

## 📊 API Testing Examples

Use the **Scalar Docs** page at `http://localhost:8080/scalar` or use `curl`:

### 1. Register a User
**POST** `/auth/register`
```bash
curl -i -X POST http://localhost:8080/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@example.com", "name": "Alice", "dob": "1990-05-10", "password": "securepassword123"}'
```

### 2. Login to get Access Token
**POST** `/auth/login`
```bash
curl -i -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice@example.com&password=securepassword123"
```
*Response returns the token:*
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Get User By ID (Protected Route)
**GET** `/users/1`
```bash
curl -i http://localhost:8080/users/1 \
  -H "Authorization: Bearer <your_access_token>"
```
*Expected Response (including dynamic age calculation):*
```json
{
  "id": 1,
  "email": "alice@example.com",
  "name": "Alice",
  "dob": "1990-05-10",
  "age": 36
}
```

### 4. Logout (Blacklist Token)
**POST** `/auth/logout`
```bash
curl -i -X POST http://localhost:8080/auth/logout \
  -H "Authorization: Bearer <your_access_token>"
```
*Subsequent calls using the blacklisted token will return HTTP `401 Unauthorized`.*
