# 🔧 Guia de Instalação

## 📦 Passo a Passo

### 1. Instalar Python
1. Baixe em: https://www.python.org/
2. Instale marcando "Add Python to PATH"
3. Verifique:
```bash
python --version
```

### 2. Executar Instalação
```bash
scripts\install.bat
```

### 3. Configurar Credenciais
1. Coloque `account.json` na raiz do projeto
2. Compartilhe a planilha com o email do service account

### 4. Executar
```bash
scripts\start-dashboard-dash.bat
```

## ❓ Preciso de Node.js?

### ❌ NÃO precisa se:
- Usar apenas Dashboard Dash
- Quer algo simples e rápido

### ✅ SIM precisa se:
- Usar Frontend React
- Quer interface moderna

## 🔧 Instalação Manual

### Backend (Python):
```bash
cd backend
pip install -r requirements.txt
cd ..
```

### Frontend (React) - Opcional:
```bash
cd frontend
npm install
cd ..
```

## ✅ Verificar Instalação

### Python:
```bash
python --version
pip list | findstr fastapi
```

### Node.js (opcional):
```bash
node --version
npm --version
```

### Frontend instalado:
```bash
dir frontend\node_modules
```

## 🚀 Executar

### Dashboard Dash (Apenas Python):
```bash
scripts\start-dashboard-dash.bat
```
Acesse: http://localhost:8051

### Backend API + Frontend React:
```bash
# Terminal 1
scripts\start-backend-api.bat

# Terminal 2
scripts\start-frontend-react.bat
```
Acesse: http://localhost:5173

## 🐛 Erros Comuns

### "Python não encontrado"
**Solução:** Instale Python e marque "Add to PATH"

### "Node.js não encontrado"
**Solução:** 
- Se usar Dashboard Dash: ignore, não precisa
- Se usar Frontend React: instale Node.js

### "account.json não encontrado"
**Solução:** Coloque o arquivo na raiz do projeto

### "Caminho não encontrado"
**Solução:** Execute os scripts .bat a partir da raiz do projeto

## 💡 Dica

**Começando?** Use apenas o Dashboard Dash:
1. Instale Python
2. Execute `scripts\install.bat`
3. Execute `scripts\start-dashboard-dash.bat`

Não precisa de Node.js! 🎯
