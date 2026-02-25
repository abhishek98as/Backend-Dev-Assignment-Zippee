# Task Manager API

A simple REST API built with Django and Django REST Framework. It lets users manage tasks with full CRUD operations, JWT based authentication, and role based access control. Swagger docs are also included for easy API testing.

---

## Tech Stack

- Python 3.14
- Django 4.2
- Django REST Framework
- djangorestframework-simplejwt (JWT auth)
- drf-yasg (Swagger documentation)
- django-filter (filtering support)
- SQLite (default database, no setup needed)

---

## Project Setup

### 1. Clone the repository

```
git clone <your-repo-url>
cd task-manager
```

### 2. Create a virtual environment

```
python -m venv venv
```

Activate it:

- On Windows: `venv\Scripts\activate`
- On Mac/Linux: `source venv/bin/activate`

### 3. Install dependancies

```
pip install -r requirements.txt
```

### 4. Run migrations

```
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (optional)

If you want to access the Django admin panel:

```
python manage.py createsuperuser
```

---

## Running the App

```
python manage.py runserver
```

The app will start at `http://127.0.0.1:8000/`

- Frontend UI: `http://127.0.0.1:8000/`
- Swagger docs: `http://127.0.0.1:8000/api/swagger/`
- Django Admin: `http://127.0.0.1:8000/admin/`

---

## Running Tests

To run all unit tests:

```
python manage.py test accounts tasks
```

To run with more detail:

```
python manage.py test accounts tasks --verbosity=2
```

There are 16 tests in total covering registration, login, task CRUD, and permission checks.

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register/ | Register a new user |
| POST | /api/auth/login/ | Login and get JWT tokens |

**Register example:**

```
POST /api/auth/register/
{
    "username": "john",
    "password": "mypassword123",
    "email": "john@example.com"
}
```

**Login example:**

```
POST /api/auth/login/
{
    "username": "john",
    "password": "mypassword123"
}
```

Response will include `access` and `refresh` tokens. Use the `access` token in the Authorization header for protected endpoints:

```
Authorization: Bearer <access_token>
```

---

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/tasks/ | Get all tasks |
| POST | /api/tasks/ | Create a new task (auth required) |
| GET | /api/tasks/{id}/ | Get a single task |
| PUT | /api/tasks/{id}/ | Update a task (owner or admin only) |
| DELETE | /api/tasks/{id}/ | Delete a task (owner or admin only) |

**Create task example:**

```
POST /api/tasks/
Authorization: Bearer <token>
{
    "title": "Buy groceries",
    "description": "milk, eggs, bread",
    "completed": false
}
```

**Filter by status:**

```
GET /api/tasks/?completed=true
GET /api/tasks/?completed=false
```

**Pagination:**

```
GET /api/tasks/?page=2
```

Page size is 10 by default.

---

## User Roles

There are two roles in the system:

- **user** (default) - can create tasks and manage their own tasks only
- **admin** - can view and manage all tasks from all users

When registering you can pass `"role": "admin"` to create an admin account. In a real production app this should be restircted ofcourse.

---

## Swagger Docs

Full interactive API documentation is available at:

```
http://127.0.0.1:8000/api/swagger/
```

You can test all endpoints directly from the browser. To use protected endpoints in Swagger, click Authorize and enter `Bearer <your_token>`.

---

## Notes

- The project uses SQLite so there is no database setup needed. The `db.sqlite3` file is created automaticaly when you run migrations.
- JWT access tokens expire after 60 minutes. You can use the refresh token to get a new one if needed.
- The frontend at `/` is a simple Bootstrap page for doing CRUD operations visually. Its not fancy but it works.
- Tests use an in-memory database so they dont affect your local data.
