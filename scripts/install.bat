@echo off
cls
echo ================================================================================
echo                  INSTALACAO - DASHBOARD DE MONITORAMENTO
echo ================================================================================
echo.

REM Vai para a raiz do projeto
cd /d "%~dp0.."

REM Verifica Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Instale Python 3.8+ em: https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo [1/2] Instalando dependencias Python (Backend)...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar Python!
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo [2/2] Instalando dependencias Frontend (React)...
echo.
echo NOTA: Se voce NAO tem Node.js instalado, pode pular esta etapa.
echo       O Dashboard Dash funciona apenas com Python!
echo.

REM Verifica se Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [AVISO] Node.js nao encontrado!
    echo.
    echo Opcoes:
    echo   1. Instale Node.js em: https://nodejs.org/
    echo   2. Ou use apenas o Dashboard Dash (nao precisa de Node.js)
    echo.
    echo Pulando instalacao do Frontend...
    goto :fim
)

cd frontend
call npm install
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar Frontend!
    cd ..
    pause
    exit /b 1
)
cd ..

:fim
echo.
echo ================================================================================
echo                          INSTALACAO CONCLUIDA!
echo ================================================================================
echo.
echo Para executar:
echo   Dashboard Dash:  scripts\start-dashboard-dash.bat
echo.
echo Se instalou Node.js:
echo   Backend API:     scripts\start-backend-api.bat
echo   Frontend React:  scripts\start-frontend-react.bat
echo.
pause
