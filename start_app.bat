@echo off
echo Starting TailorTalk Application...
echo.
echo 1. Starting FastAPI Backend on port 8004...
start "FastAPI Backend" cmd /k "uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload"
echo.
echo 2. Starting Streamlit Frontend on port 8501...
start "Streamlit Frontend" cmd /k "streamlit run streamlit_app/frontend.py"
echo.
echo 3. Starting Ollama (TinyLlama)...
start "Ollama" cmd /k ""C:\Users\jayas\AppData\Local\Programs\Ollama\ollama.exe" run tinyllama"
echo.
echo Application URLs:
echo - FastAPI Backend: http://localhost:8004
echo - API Docs: http://localhost:8004/docs
echo - Streamlit Frontend: http://localhost:8501
echo.
echo Press any key to exit this script...
pause 