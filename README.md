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

