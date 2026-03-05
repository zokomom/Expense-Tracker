# 💸 Expense Tracker API

A RESTful API for tracking personal expenses, built with **FastAPI** and **PostgreSQL**. Features JWT authentication, user management, and full CRUD operations with flexible expense filtering.

---

## 🚀 Features

- **User Authentication** — Sign up and log in with JWT-based session management
- **Expense Management** — Create, read, update, and delete expenses
- **Expense Filtering** — Filter expenses by:
  - Past week
  - Past month
  - Last 3 months
  - Custom date range (dd-mm-yyyy)
- **Category Support** — User defined, any category string is accepted
- **Search by Category** — Filter expenses by category name using the `search` query param
- **Secure Passwords** — Bcrypt hashing via Passlib

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Web framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Alembic | Database migrations |
| Passlib + Bcrypt | Password hashing |
| Python-Jose | JWT handling |
| Pydantic | Data validation |

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/zokomom/Expense-Tracker.git
cd Expense-Tracker
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5433/your_db_name
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run database migrations
```bash
alembic upgrade head
```

### 6. Start the server
```bash
uvicorn app.main:app --reload
```

---

## 📁 Project Structure

```
Expense-Tracker/
├── alembic/              # Database migrations
│   └── versions/
├── app/
│   ├── routers/
│   │   ├── users.py      # User registration
│   │   ├── login.py      # Authentication
│   │   └── expenses.py   # Expense CRUD
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── database.py       # DB connection
│   ├── oauth2.py         # JWT logic
│   ├── utils.py          # Password hashing
│   ├── config.py         # Environment settings
│   └── main.py           # App entry point
├── alembic.ini
├── requirements.txt
└── .gitignore
```

---

## 📌 API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/users` | Register a new user |
| POST | `/login` | Login and get JWT token |

### Expenses
| Method | Endpoint | Description |
|---|---|---|
| GET | `/expenses` | Get all expenses (with filters) |
| POST | `/expenses` | Create a new expense |
| GET | `/expenses/{id}` | Get a single expense |
| PUT | `/expenses/{id}` | Update an expense |
| DELETE | `/expenses/{id}` | Delete an expense |

### Filtering Query Params
```
GET /expenses?filter=past_week
GET /expenses?filter=past_month
GET /expenses?filter=last_3_months
GET /expenses?filter=custom&start_date=01-01-2025&end_date=31-03-2025
GET /expenses?search=Food        # search by any category name
```

---

## 🔐 Authentication

All `/expenses` endpoints require a valid JWT token in the request header:

```
Authorization: Bearer <your_token>
```

Get the token by calling `POST /login` with your credentials.

---

## 📖 API Documentation

Once the server is running, visit:
- **Swagger UI** → http://localhost:8000/docs
- **ReDoc** → http://localhost:8000/redoc

---

## 🙏 Credits

This project is based on the [Expense Tracker API](https://roadmap.sh/projects/expense-tracker) project from [roadmap.sh](https://roadmap.sh).
[https://roadmap.sh/projects/expense-tracker-api](https://roadmap.sh/projects/expense-tracker-api)

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).
