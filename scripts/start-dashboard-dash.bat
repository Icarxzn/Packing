@echo off
echo Iniciando Dashboard Dash...
echo URL: http://localhost:8051
echo.

REM Vai para a raiz do projeto
cd /d "%~dp0.."

REM Entra na pasta backend
cd backend

REM Executa o Monitoramento.py
python Monitoramento.py

pause
