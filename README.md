# Dashboard de Monitoramento de Viagens

## 🚀 Início Rápido

### 1. Instalar
```bash
scripts\install.bat
```

### 2. Configurar
1. Coloque `account.json` na raiz do projeto
2. Edite `backend/main.py` ou `backend/Monitoramento.py`:
```python
PLANILHA_ID = "SEU_ID"
NOME_ABA = "Sua Aba"
```

### 3. Executar
```bash
scripts\start-dashboard-dash.bat
```

## 📋 Requisitos

### Dashboard Dash (Recomendado)
- ✅ Python 3.8+
- ❌ Node.js (não precisa)

### Frontend React (Opcional)
- ✅ Python 3.8+
- ✅ Node.js 16+

## 🎯 Opções de Interface

### Opção 1: Dashboard Dash (Simples)
```bash
scripts\start-dashboard-dash.bat
```
- Porta: 8051
- Apenas Python
- Interface completa

### Opção 2: Backend API + Frontend React (Moderno)
```bash
# Terminal 1
scripts\start-backend-api.bat

# Terminal 2
scripts\start-frontend-react.bat
```
- Backend: 8000
- Frontend: 5173
- Precisa de Node.js

## 📁 Estrutura
```
├── backend/              # Backend Python
│   ├── main.py          # API REST
│   └── Monitoramento.py # Dashboard Dash
├── frontend/            # Frontend React
│   └── src/
├── scripts/             # Scripts de execução
│   ├── install.bat
│   ├── start-dashboard-dash.bat
│   ├── start-backend-api.bat
│   └── start-frontend-react.bat
└── account.json         # Credenciais
```

## 🐛 Troubleshooting

**Python não encontrado:**
- Instale em: https://www.python.org/

**Node.js não encontrado:**
- Só precisa se usar Frontend React
- Instale em: https://nodejs.org/

**account.json não encontrado:**
- Coloque na raiz do projeto

**Porta em uso:**
```bash
netstat -ano | findstr :8051
taskkill /PID <PID> /F
```
