@echo off
echo Iniciando Frontend React...
echo URL: http://localhost:5173
echo.

REM Vai para a raiz do projeto
cd /d "%~dp0.."

REM Entra na pasta frontend
cd frontend

REM Executa npm run dev
call npm run dev

pause
