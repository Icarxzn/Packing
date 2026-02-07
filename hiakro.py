import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

print("="*70)
print("INICIANDO DASHBOARD NOVO")
print("="*70)

# Config
PLANILHA_ID = "1BKB3rsrZFcHxRt0LkTABtSBlqv7VWU6TwmkbwX95TLI"
NOME_ABA = "Base Principal"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Cache global para evitar muitas requisições
dados_cache = {"df": None, "timestamp": None}
CACHE_DURATION = 60  # segundos

def carregar_dados():
    import time
    global dados_cache
    
    # Verificar se tem cache válido
    if dados_cache["df"] is not None and dados_cache["timestamp"] is not None:
        tempo_decorrido = time.time() - dados_cache["timestamp"]
        if tempo_decorrido < CACHE_DURATION:
            print(f"Usando cache ({int(CACHE_DURATION - tempo_decorrido)}s restantes)")
            return dados_cache["df"]
    
    print("Conectando ao Google Sheets...")
    creds = Credentials.from_service_account_file("account.json", scopes=SCOPES)
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(PLANILHA_ID).worksheet(NOME_ABA)
    print("Conectado!")
    
    all_values = sheet.get_all_values()
    df = pd.DataFrame(all_values[1:], columns=all_values[0])
    df = df.dropna(how='all')
    
    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    
    print(f"{len(df)} linhas, {len(df.columns)} colunas carregadas")
    
    # Atualizar cache
    dados_cache["df"] = df
    dados_cache["timestamp"] = time.time()
    
    return df

# Carregar dados no início
df_inicial = carregar_dados()
print("="*70 + "\n")

# App
app = dash.Dash(__name__)
app.title = "Dashboard de Monitoramento de Viagens"

# CSS profissional com gradientes laranja
app.index_string = '''<!DOCTYPE html><html><head>{%metas%}<title>{%title%}</title>{%favicon%}{%css%}<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Poppins',sans-serif;background:linear-gradient(135deg,#fff5f0 0%,#ffe8dd 50%,#ffd4c4 100%);min-height:100vh;padding:20px}
#react-entry-point{max-width:1600px;margin:0 auto}

/* Header com gradiente laranja */
.title-container{background:linear-gradient(135deg,#FF6B35 0%,#FF8C42 50%,#FFB085 100%);padding:35px 40px;border-radius:16px;margin-bottom:25px;box-shadow:0 8px 24px rgba(255,107,53,.25)}
.title-gradient{color:white;font-weight:700;font-size:2rem;margin:0;margin-bottom:5px;text-shadow:2px 2px 4px rgba(0,0,0,.1)}
.header-subtitle{color:rgba(255,255,255,.95);font-size:1rem;font-weight:400}

/* Filtros com gradiente suave */
.filters-container{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:25px;padding:25px;background:linear-gradient(135deg,#ffffff 0%,#fff5f0 100%);border-radius:16px;box-shadow:0 4px 16px rgba(255,107,53,.1);border:2px solid #ffe8dd}
.filter-item{display:flex;flex-direction:column}
.filter-item label{font-weight:600;color:#FF6B35;margin-bottom:8px;font-size:.9rem}

/* Dropdown styling */
.Select-control{border:2px solid #ffe8dd!important;border-radius:8px!important;transition:all .2s ease!important;background:white!important;min-height:42px!important}
.Select-control:hover{border-color:#FF8C42!important;box-shadow:0 0 0 3px rgba(255,107,53,.1)!important}
.Select-control.is-focused{border-color:#FF6B35!important;box-shadow:0 0 0 3px rgba(255,107,53,.15)!important}

/* Grafico com gradiente */
.graphs-container{margin-bottom:25px}
.graph-card{background:linear-gradient(135deg,#ffffff 0%,#fffaf7 100%);border-radius:16px;padding:25px;box-shadow:0 4px 16px rgba(255,107,53,.1);border:2px solid #ffe8dd;transition:all .3s ease;position:relative;overflow:hidden}
.graph-card::before{content:'';position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,#FF6B35 0%,#FF8C42 50%,#FFB085 100%)}
.graph-card:hover{box-shadow:0 8px 24px rgba(255,107,53,.2);transform:translateY(-2px);border-color:#ffd4c4}

/* Tabela */
h3{color:#FF6B35;font-size:1.5rem;margin-bottom:20px;font-weight:700;padding-left:5px;position:relative}
h3::after{content:'';position:absolute;bottom:-5px;left:5px;width:60px;height:3px;background:linear-gradient(90deg,#FF6B35,#FF8C42);border-radius:2px}
.table-container{background:linear-gradient(135deg,#ffffff 0%,#fffaf7 100%);border-radius:16px;padding:25px;box-shadow:0 4px 16px rgba(255,107,53,.1);border:2px solid #ffe8dd}
.dash-table-container{border-radius:12px;overflow:hidden;border:2px solid #ffe8dd}
.dash-spreadsheet{font-size:.9rem}
.dash-table-header{background:linear-gradient(135deg,#FF6B35 0%,#FF8C42 100%)!important;color:white!important;font-weight:600!important}
.dash-table-header th{background:inherit!important;color:white!important;border-right:1px solid rgba(255,255,255,.15)!important;padding:16px!important}
.dash-table-row{border-bottom:1px solid #ffe8dd;transition:background .2s ease}
.dash-table-row:hover{background:linear-gradient(135deg,#fff5f0 0%,#ffe8dd 100%)!important}
.dash-table-cell{padding:14px!important}
.dash-filter{background:linear-gradient(135deg,#fff5f0,#ffe8dd)!important;border-bottom:2px solid #ffd4c4!important}

/* Responsive */
@media (max-width:1024px){
.filters-container{grid-template-columns:1fr}
.title-gradient{font-size:1.6rem}
}

/* Scrollbar laranja */
::-webkit-scrollbar{width:8px;height:8px}
::-webkit-scrollbar-track{background:#ffe8dd;border-radius:4px}
::-webkit-scrollbar-thumb{background:linear-gradient(135deg,#FF6B35,#FF8C42);border-radius:4px}
::-webkit-scrollbar-thumb:hover{background:linear-gradient(135deg,#FF8C42,#FFB085)}
</style></head><body>{%app_entry%}{%config%}{%scripts%}{%renderer%}</body></html>'''

app.layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.H1("Dashboard de Monitoramento de Viagens", className="title-gradient"),
            html.Div("Acompanhe suas operacoes logisticas em tempo real", className="header-subtitle")
        ])
    ], className="title-container"),
    
    dcc.Interval(id="interval", interval=60000, n_intervals=0),  # Atualiza a cada 60 segundos
    
    # Filtros
    html.Div([
        html.Div([
            html.Label("ID (LT)"),
            dcc.Dropdown(id="filtro-id", multi=True, placeholder="Selecione os LTs...", options=[])
        ], className="filter-item"),
        
        html.Div([
            html.Label("Destino"),
            dcc.Dropdown(id="filtro-destino", multi=True, placeholder="Selecione destinos...", options=[])
        ], className="filter-item"),
        
        html.Div([
            html.Label("Status da Viagem"),
            dcc.Dropdown(id="filtro-status", multi=True, placeholder="Selecione status...", options=[])
        ], className="filter-item"),
        
        html.Div([
            html.Div([
                html.Label("Data Inicial"),
                dcc.DatePickerSingle(
                    id="filtro-data-inicial",
                    display_format="DD/MM/YYYY",
                    placeholder="Selecione a data inicial",
                    style={'width': '100%'}
                )
            ], className="filter-item"),
            
            html.Div([
                html.Label("Data Final"),
                dcc.DatePickerSingle(
                    id="filtro-data-final",
                    display_format="DD/MM/YYYY",
                    placeholder="Selecione a data final",
                    style={'width': '100%'}
                )
            ], className="filter-item")
        ], style={'gridColumn': '1 / -1', 'display': 'grid', 'gridTemplateColumns': 'repeat(2, 300px)', 'gap': '20px', 'justifyContent': 'center', 'marginTop': '10px'})
    ], className="filters-container"),
    
    # Grafico
    html.Div([
        html.Div([
            dcc.Graph(id="grafico")
        ], className="graph-card")
    ], className="graphs-container"),
    
    # Tabela
    html.Div([
        html.Div([
            html.H3("Dados Detalhados", style={'display': 'inline-block', 'marginBottom': '0'}),
            html.Button(
                "📥 Exportar CSV",
                id="btn-exportar",
                style={
                    'float': 'right',
                    'background': 'linear-gradient(135deg, #28a745, #20c997)',
                    'color': 'white',
                    'border': 'none',
                    'padding': '12px 24px',
                    'borderRadius': '8px',
                    'cursor': 'pointer',
                    'fontWeight': '600',
                    'fontSize': '0.95rem',
                    'boxShadow': '0 4px 12px rgba(40, 167, 69, 0.3)',
                    'transition': 'all 0.3s ease'
                }
            ),
            dcc.Download(id="download-csv")
        ], style={'marginBottom': '20px', 'overflow': 'hidden'}),
        
        dash_table.DataTable(
            id="tabela",
            page_size=25,
            sort_action="native",
            filter_action="native",
            style_table={"borderRadius": "6px", "height": "600px", "overflowY": "auto"},
            style_cell={
                "padding": "12px",
                "textAlign": "left",
                "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
                "fontSize": "13px",
                "whiteSpace": "normal",
                "height": "auto"
            },
            style_header={
                "fontWeight": "700",
                "backgroundColor": "#FF6B35",
                "color": "white",
                "borderBottom": "2px solid #FF8C42",
                "fontSize": "14px",
                "padding": "15px",
                "textAlign": "center"
            },
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "#FFF5F0"
                },
                {
                    "if": {"row_index": "even"},
                    "backgroundColor": "white"
                }
            ],
            style_filter={
                "backgroundColor": "#FFE8DD",
                "fontWeight": "600"
            }
        )
    ], className="table-container")
], style={"maxWidth": "1400px", "margin": "0 auto"})

@app.callback(
    Output("filtro-id", "options"),
    Output("filtro-destino", "options"),
    Output("filtro-status", "options"),
    Input("interval", "n_intervals")
)
def atualizar_filtros(_):
    df = carregar_dados()
    ids = sorted(df["trip_number"].unique()) if "trip_number" in df.columns else []
    destinos = sorted(df["destination_station_code"].unique()) if "destination_station_code" in df.columns else []
    status = sorted(df["Status_da_Viagem"].unique()) if "Status_da_Viagem" in df.columns else []
    return (
        [{"label": str(i), "value": i} for i in ids],
        [{"label": str(d), "value": d} for d in destinos],
        [{"label": str(s), "value": s} for s in status]
    )

@app.callback(
    Output("grafico", "figure"),
    Output("tabela", "columns"),
    Output("tabela", "data"),
    Input("filtro-id", "value"),
    Input("filtro-destino", "value"),
    Input("filtro-status", "value"),
    Input("filtro-data-inicial", "date"),
    Input("filtro-data-final", "date"),
    Input("interval", "n_intervals")
)
def atualizar_dashboard(ids, destinos, status, data_inicial, data_final, _):
    df = carregar_dados()
    
    # Filtros
    if ids and "trip_number" in df.columns:
        df = df[df["trip_number"].isin(ids)]
    if destinos and "destination_station_code" in df.columns:
        df = df[df["destination_station_code"].isin(destinos)]
    if status and "Status_da_Viagem" in df.columns:
        df = df[df["Status_da_Viagem"].isin(status)]
    
    # Filtro de data
    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
        
        if data_inicial:
            data_inicial_dt = pd.to_datetime(data_inicial)
            df = df[df["Data"] >= data_inicial_dt]
        
        if data_final:
            data_final_dt = pd.to_datetime(data_final)
            df = df[df["Data"] <= data_final_dt]
    
    # Gráfico separado por Status_da_Viagem
    if "Data" in df.columns:
        df_data = df.copy()
        df_data["Data"] = pd.to_datetime(df_data["Data"], errors="coerce")
        df_data = df_data.dropna(subset=["Data"])
        
        if not df_data.empty and "Status_da_Viagem" in df_data.columns:
            # Agrupar por data e status
            contagem = df_data.groupby([df_data["Data"].dt.date, "Status_da_Viagem"]).size().reset_index()
            contagem.columns = ["Data", "Status", "Quantidade"]
            
            # Criar gráfico de barras agrupadas (lado a lado) com cores por status
            fig = px.bar(
                contagem,
                x="Data",
                y="Quantidade",
                color="Status",
                title="Viagens por Data e Status",
                color_discrete_map={
                    "Parado": "#dc3545",  # Vermelho
                    "Em trânsito": "#28a745",  # Verde
                    "Em transito": "#28a745",  # Verde (sem acento)
                    "Finalizado": "#6c757d",  # Cinza
                    "Cancelado": "#ffc107"  # Amarelo
                },
                barmode="group",  # Barras lado a lado (agrupadas)
                text="Quantidade"  # Mostra o valor em cima da barra
            )
            fig.update_traces(textposition='outside')  # Posiciona o texto fora da barra
            fig.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                xaxis_title="Data",
                yaxis_title="Quantidade de Viagens",
                legend_title="Status da Viagem"
            )
        else:
            fig = go.Figure().add_annotation(text="Sem dados")
    else:
        fig = go.Figure().add_annotation(text="Coluna Data não encontrada")
    
    # Tabela - Colunas E, AB, AT, C, B, AC (trip_number, Status_da_Viagem, ETA Planejado, Ultima localização, Previsão de chegada, Ocorrencia)
    colunas = ["trip_number", "Status_da_Viagem", "ETA Planejado", "Ultima localização", "Previsão de chegada", "Ocorrencia"]
    colunas_existentes = [c for c in colunas if c in df.columns]
    
    if colunas_existentes:
        df_tabela = df[colunas_existentes]
    else:
        df_tabela = df
        colunas_existentes = df.columns.tolist()
    
    columns = [{"name": c, "id": c} for c in colunas_existentes]
    
    return fig, columns, df_tabela.to_dict("records")

@app.callback(
    Output("download-csv", "data"),
    Input("btn-exportar", "n_clicks"),
    Input("filtro-id", "value"),
    Input("filtro-destino", "value"),
    Input("filtro-status", "value"),
    Input("filtro-data-inicial", "date"),
    Input("filtro-data-final", "date"),
    prevent_initial_call=True
)
def exportar_csv(n_clicks, ids, destinos, status, data_inicial, data_final):
    if not n_clicks:
        return None
    
    df = carregar_dados()
    
    # Aplicar os mesmos filtros
    if ids and "trip_number" in df.columns:
        df = df[df["trip_number"].isin(ids)]
    if destinos and "destination_station_code" in df.columns:
        df = df[df["destination_station_code"].isin(destinos)]
    if status and "Status_da_Viagem" in df.columns:
        df = df[df["Status_da_Viagem"].isin(status)]
    
    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
        
        if data_inicial:
            data_inicial_dt = pd.to_datetime(data_inicial)
            df = df[df["Data"] >= data_inicial_dt]
        
        if data_final:
            data_final_dt = pd.to_datetime(data_final)
            df = df[df["Data"] <= data_final_dt]
    
    # Selecionar apenas as colunas da tabela
    colunas = ["trip_number", "Status_da_Viagem", "ETA Planejado", "Ultima localização", "Previsão de chegada", "Ocorrencia"]
    colunas_existentes = [c for c in colunas if c in df.columns]
    
    if colunas_existentes:
        df_export = df[colunas_existentes]
    else:
        df_export = df
    
    return dcc.send_data_frame(df_export.to_csv, "dados_viagens.csv", index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    print("\n" + "="*70)
    print("Dashboard rodando em:")
    print("  Local: http://127.0.0.1:8051/")
    print("  Rede:  http://SEU_IP:8051/")
    print("\nPara descobrir seu IP, rode: ipconfig")
    print("="*70 + "\n")
    app.run(debug=True, host='0.0.0.0', port=8051)
