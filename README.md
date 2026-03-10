# Sundaram Digital Management System

A full-stack business management application for Sundaram Digital, built with Angular (frontend) and Python FastAPI (backend).

## Prerequisites

- **Node.js** (v16 or later) and **npm**
- **Angular CLI** (`npm install -g @angular/cli`)
- **Python** (v3.9 or later)

---

## Running the Project

You need to open **two separate terminals** — one for the backend and one for the frontend.

---

### Terminal 1 — Backend (Python / FastAPI)

```bash
# Navigate to the backend directory
cd backend

# (First time only) Create and activate a virtual environment
python -m venv venv

# Activate on Linux/macOS:
source venv/bin/activate

# Activate on Windows:
# venv\Scripts\activate

# (First time only) Install Python dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn app:app --reload --port 8000
```

The backend API will be available at: **http://localhost:8000**

API docs (Swagger UI): **http://localhost:8000/docs**

---

### Terminal 2 — Frontend (Angular)

```bash
# Navigate to the frontend directory
cd frontend

# (First time only) Install Node.js dependencies
npm install

# Start the Angular development server
ng serve
```

The frontend will be available at: **http://localhost:4200**

---

## Login Credentials

| Username | Password  |
|----------|-----------|
| admin    | admin123  |

---

## Project Structure

```
sundaram-digital-system/
├── backend/                  # Python FastAPI backend
│   ├── app.py                # Main FastAPI application
│   ├── requirements.txt      # Python dependencies
│   ├── models/
│   │   └── database.py       # SQLAlchemy models & DB setup
│   └── routes/               # API route handlers
│       ├── auth.py
│       ├── customers.py
│       ├── orders.py
│       ├── points.py
│       ├── reports.py
│       └── backup.py
├── frontend/                 # Angular frontend
│   ├── src/
│   │   └── app/
│   │       ├── components/   # UI components
│   │       └── services/     # HTTP service layer
│   └── package.json
└── system.config.json        # System configuration
```

---

## Configuration

Edit `system.config.json` in the root directory to change:

- Business name
- Frontend/backend ports
- Database name
- Points system settings

> **Note:** If you change the backend port in `system.config.json`, update `private apiUrl` in all frontend service files accordingly.

---

## Database

The SQLite database is automatically created at `database/database.db` when the backend starts for the first time. No manual setup is required.

To create a database backup, use the **Backup** page in the application UI.
