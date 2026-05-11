# E-Commerce REST API

Backend REST API for an e-commerce web application built with FastAPI.

## Features

### Authentication & Authorization
- User registration
- JWT authentication
- Password hashing with bcrypt/passlib
- Role-based access control (User/Admin)

### Products
- Product CRUD operations
- Product search
- Filtering by category and price
- Pagination

### Cart
- Add products to cart
- Remove products from cart
- View cart contents

### Orders
- Create orders from cart
- Order history
- Order status management

### Favorites
- Add products to favorites
- Remove from favorites
- View favorite products

### Messages
- Send messages from users (via Contact us)
- Admin message management

### Email Notifications
- Registration email
- Order creation email
- Order status update email

---

# Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Pydantic
- Resend Email API

---

# Project Structure

```text
project/
├── core/
├── routers/
├── services/
├── models/
├── schemas/
├── db.py
├── main.py
├── requirements.txt
└── .env





## Installation

### 1. Clone the repository

```bash
git clone <repository_url>
cd <project_name>
```

---

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the environment:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/db_name

SECRET_KEY=your_secret_key
ALGORITHM=HS256

RESEND_API_KEY=your_resend_api_key
EMAIL_FROM=onboarding@resend.dev
```

---

### 5. Run the application

```bash
uvicorn main:app --reload
```





## API Documentation & Testing

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

Interactive API documentation and endpoint testing.

---

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

Alternative API documentation interface.