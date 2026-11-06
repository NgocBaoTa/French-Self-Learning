# Mon français

Local French-learning website for Vietnamese learners, running on Windows.

## Requirements

- Windows PowerShell
- Python 3.10+
- Node.js 20+ and npm

## Install the backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python seed.py
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass`.

Create an administrator account with your own password:

```powershell
python create_admin.py --username admin --password "ChooseAStrongPassword"
```

## Install the frontend

In a second PowerShell window:

```powershell
cd frontend
npm install
```

## Run locally

Backend:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python app.py
```

Frontend:

```powershell
cd frontend
npm run dev
```

Open <http://localhost:5173>. Vite proxies `/api` requests to Flask at `http://127.0.0.1:5000`.

## Build and test

```powershell
cd frontend
npm run build

cd ..\backend
.\.venv\Scripts\Activate.ps1
python -m unittest discover tests -v
```

## Local data and backups

The local database is stored at `backend/instance/monfrancais.sqlite3`. Stop Flask before backing it up:

```powershell
Copy-Item backend\instance\monfrancais.sqlite3 .\backup-monfrancais.sqlite3
```

To restore a backup, stop Flask and copy the backup back to `backend/instance/monfrancais.sqlite3`. The seed script is idempotent and can be run again without deleting learner progress.

## Troubleshooting

- If `python` is not recognized, install Python and enable “Add Python to PATH”, then open a new PowerShell window.
- If activation is blocked, run `Set-ExecutionPolicy -Scope Process Bypass`.
- If port 5000 is busy, set `FLASK_PORT=5001` in `.env` and update the proxy in `frontend/vite.config.js`.
- To start with a fresh local database, stop the app and delete only `backend/instance/monfrancais.sqlite3`, then run `python seed.py`.
