@echo off
echo Starting Backend and Frontend...

:: Start Backend in a new window (with venv activated)
start cmd /k ".venv\Scripts\activate && cd backend && uvicorn main:app --reload"

:: Start Frontend in the current window
cd frontend
npm start
