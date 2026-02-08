@echo off
echo Iniciando Backend API...
echo URL: http://localhost:8000
echo Docs: http://localhost:8000/docs
echo.

REM Vai para a raiz do projeto
cd /d "%~dp0.."

REM Entra na pasta backend
cd backend

REM Executa o main.py
python main.py

pause
