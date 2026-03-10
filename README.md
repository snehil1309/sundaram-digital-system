# Sundaram Digital System

A full-stack business management system for Sundaram Digital, built with Angular (frontend) and FastAPI (backend).

## Project Structure

```
sundaram-digital-system/
├── frontend/        # Angular 16 application (runs on port 4200)
├── backend/         # FastAPI application (runs on port 8000)
└── system.config.json
```

## Prerequisites

- [Node.js](https://nodejs.org/) (v16 or later)
- [Python](https://www.python.org/) (v3.9 or later)
- [VS Code](https://code.visualstudio.com/)

## Getting Started in VS Code

1. **Open the project** in VS Code:
   ```
   code .
   ```

2. **Install recommended extensions** when prompted, or open the Extensions view and search for `@recommended`.

3. **Set up the backend**:
   ```bash
   cd backend
   python -m venv .venv
   # On Windows: .venv\Scripts\activate
   # On macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   python init_db.py
   ```

4. **Set up the frontend**:
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

### Using VS Code Tasks (Recommended)

Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run:
- **`Tasks: Run Task` → `Start Full Stack`** — starts both backend and frontend simultaneously
- **`Tasks: Run Task` → `Start Backend`** — starts only the FastAPI backend
- **`Tasks: Run Task` → `Start Frontend`** — starts only the Angular frontend

### Using the Terminal

**Backend** (from the `backend/` directory):
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Frontend** (from the `frontend/` directory):
```bash
npm start
```

Once running:
- Frontend: [http://localhost:4200](http://localhost:4200)
- Backend API: [http://localhost:8000](http://localhost:8000)
- API Docs (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)

## Debugging in VS Code

Open the **Run and Debug** panel (`Ctrl+Shift+D` / `Cmd+Shift+D`) and select:
- **`Debug Backend (FastAPI)`** — debugs the Python backend with breakpoint support
- **`Debug Frontend (Chrome)`** — debugs the Angular app in Chrome with source maps
- **`Debug Full Stack`** — launches both debuggers simultaneously

## Configuration

Application settings are stored in [`system.config.json`](system.config.json):
- `frontendPort`: Angular dev server port (default: `4200`)
- `backendPort`: FastAPI server port (default: `8000`)
- `database`: SQLite database settings
- `pointsSystem`: Loyalty points configuration
