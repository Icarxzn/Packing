"""
Backend API - Dashboard de Monitoramento de Viagens
API REST para servir dados do Google Sheets ao frontend React
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import time
from typing import Optional
import uvicorn
from pathlib import Path

# ==================== CONFIGURAÇÕES ====================

PLANILHA_ID = "1BKB3rsrZFcHxRt0LkTABtSBlqv7VWU6TwmkbwX95TLI"
NOME_ABA = "Base Principal"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
CACHE_DURATION = 60  # segundos
API_PORT = 8000

# Cache global
dados_cache = {"df": None, "timestamp": None}

# ==================== FUNÇÕES ====================

def carregar_dados() -> pd.DataFrame:
    """Carrega dados do Google Sheets com cache"""
    global dados_cache
    
    # Verifica cache
    if dados_cache["df"] is not None and dados_cache["timestamp"] is not None:
        tempo_decorrido = time.time() - dados_cache["timestamp"]
        if tempo_decorrido < CACHE_DURATION:
            print(f"📦 Cache ({int(CACHE_DURATION - tempo_decorrido)}s restantes)")
            return dados_cache["df"]
    
    try:
        # Busca account.json na raiz do projeto
        account_path = Path(__file__).parent.parent / "account.json"
        if not account_path.exists():
            raise FileNotFoundError("account.json não encontrado na raiz do projeto!")
        
        print("🔄 Carregando dados do Google Sheets...")
        
        # Autentica e carrega
        creds = Credentials.from_service_account_file(str(account_path), scopes=SCOPES)
        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(PLANILHA_ID).worksheet(NOME_ABA)
        
        all_values = sheet.get_all_values()
        if not all_values or len(all_values) < 2:
            return pd.DataFrame()
        
        df = pd.DataFrame(all_values[1:], columns=all_values[0]).dropna(how='all')
        
        # Processa data
        if "Data" in df.columns:
            df["Data"] = pd.to_datetime(df["Data"], format='%d/%m/%Y', errors="coerce")
        
        # Atualiza cache
        dados_cache["df"] = df
        dados_cache["timestamp"] = time.time()
        
        print(f"✅ {len(df)} registros carregados")
        return df
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        raise

# ==================== FASTAPI ====================

app = FastAPI(
    title="Dashboard API",
    description="API REST para monitoramento de viagens",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== ENDPOINTS ====================

@app.get("/")
def root():
    """Status da API"""
    return {
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/data")
def get_data(
    trip_numbers: Optional[str] = Query(None, description="IDs (separados por vírgula)"),
    destinations: Optional[str] = Query(None, description="Destinos (separados por vírgula)"),
    status: Optional[str] = Query(None, description="Status (separados por vírgula)"),
    start_date: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)")
):
    """Retorna dados filtrados"""
    try:
        df = carregar_dados().copy()
        
        # Aplica filtros
        if trip_numbers and "trip_number" in df.columns:
            ids = [x.strip() for x in trip_numbers.split(",") if x.strip()]
            if ids:
                df = df[df["trip_number"].isin(ids)]
        
        if destinations and "destination_station_code" in df.columns:
            dests = [x.strip() for x in destinations.split(",") if x.strip()]
            if dests:
                df = df[df["destination_station_code"].isin(dests)]
        
        if status and "Status_da_Viagem" in df.columns:
            statuses = [x.strip() for x in status.split(",") if x.strip()]
            if statuses:
                df = df[df["Status_da_Viagem"].isin(statuses)]
        
        # Filtros de data
        if "Data" in df.columns:
            if start_date:
                df = df[df["Data"] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df["Data"] <= pd.to_datetime(end_date)]
            df["Data"] = df["Data"].dt.strftime('%Y-%m-%d')
        
        return df.to_dict(orient="records")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/filters")
def get_filters():
    """Retorna opções de filtros"""
    try:
        df = carregar_dados()
        
        return {
            "trip_numbers": sorted([str(x) for x in df["trip_number"].dropna().unique()]) if "trip_number" in df.columns else [],
            "destinations": sorted([str(x) for x in df["destination_station_code"].dropna().unique()]) if "destination_station_code" in df.columns else [],
            "status": sorted([str(x) for x in df["Status_da_Viagem"].dropna().unique()]) if "Status_da_Viagem" in df.columns else []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
def get_stats():
    """Retorna estatísticas"""
    try:
        df = carregar_dados()
        
        if "Status_da_Viagem" not in df.columns or "Data" not in df.columns:
            return {"status_counts": {}, "timeline": []}
        
        # Contagem por status
        status_counts = df["Status_da_Viagem"].value_counts().to_dict()
        
        # Timeline
        df_timeline = df.copy()
        df_timeline["Data"] = pd.to_datetime(df_timeline["Data"], errors="coerce")
        df_timeline = df_timeline.dropna(subset=["Data"])
        df_timeline["Data"] = df_timeline["Data"].dt.strftime('%Y-%m-%d')
        
        df_grouped = df_timeline.groupby(["Data", "Status_da_Viagem"]).size().reset_index()
        df_grouped.columns = ["Data", "Status", "Quantidade"]
        
        return {
            "status_counts": status_counts,
            "timeline": df_grouped.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== INICIALIZAÇÃO ====================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 BACKEND API - DASHBOARD DE MONITORAMENTO")
    print("="*70)
    print(f"📍 URL: http://localhost:{API_PORT}")
    print(f"📚 Docs: http://localhost:{API_PORT}/docs")
    print("="*70 + "\n")
    
    # Testa conexão
    try:
        print("🔍 Testando conexão...")
        carregar_dados()
        print("✅ Conexão OK!\n")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("💡 Coloque account.json na raiz do projeto\n")
        exit(1)
    except Exception as e:
        print(f"❌ Erro: {e}\n")
        exit(1)
    
    # Inicia servidor
    uvicorn.run(app, host="0.0.0.0", port=API_PORT, log_level="info")
