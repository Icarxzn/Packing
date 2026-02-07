import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import time

print("="*70)
print("INICIANDO DASHBOARD")
print("="*70)

# Configuracoes
PLANILHA_ID = "1BKB3rsrZFcHxRt0LkTABtSBlqv7VWU6TwmkbwX95TLI"
NOME_ABA = "Base Principal"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
CACHE_DURATION = 60
COLUNAS_TABELA = ["trip_number", "Status_da_Viagem", "ETA Planejado", "Ultima localização", "Previsão de chegada", "Ocorrencia"]
CORES_STATUS = {
    "Parado": "#dc3545",
    "Em trânsito": "#28a745",
    "Em transito": "#28a745",
    "Finalizado": "#6c757d",
    "Cancelado": "#ffc107"
}

dados_cache = {"df": None, "timestamp": None}

def carregar_dados():
    global dados_cache
    
    if dados_cache["df"] is not None and dados_cache["timestamp"] is not None:
        tempo_decorrido = time.time() - dados_cache["timestamp"]
        if tempo_decorrido < CACHE_DURATION:
            return dados_cache["df"]
    
    creds = Credentials.from_service_account_file("account.json", scopes=SCOPES)
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(PLANILHA_ID).worksheet(NOME_ABA)
    
    all_values = sheet.get_all_values()
    df = pd.DataFrame(all_values[1:], columns=all_values[0]).dropna(how='all')
    
    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"], format='%d/%m/%Y', errors="coerce")
    
    dados_cache["df"] = df
    dados_cache["timestamp"] = time.time()
    
    return df

carregar_dados()
print("="*70 + "\n")

app = dash.Dash(__name__)
app.title = "Dashboard de Monitoramento de Viagens"

app.index_string = '''<!DOCTYPE html><html><head>{%metas%}<title>{%title%}</title>{%favicon%}{%css%}<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Poppins',sans-serif;background:linear-gradient(135deg,#fff5f0 0%,#ffe8dd 50%,#ffd4c4 100%);min-height:100vh;padding:20px}
#react-entry-point{max-width:1600px;margin:0 auto}
.title-container{background:linear-gradient(135deg,#FF6B35 0%,#FF8C42 50%,#FFB085 100%);padding:35px 40px;border-radius:16px;margin-bottom:25px;box-shadow:0 8px 24px rgba(255,107,53,.25)}
.title-gradient{color:white;font-weight:700;font-size:2rem;margin:0;margin-bottom:5px;text-shadow:2px 2px 4px rgba(0,0,0,.1)}
.header-subtitle{color:rgba(255,255,255,.95);font-size:1rem;font-weight:400}
.filters-container{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:25px;padding:25px;background:linear-gradient(135deg,#ffffff 0%,#fff5f0 100%);border-radius:16px;box-shadow:0 4px 16px rgba(255,107,53,.1);border:2px solid #ffe8dd}
.filter-item{display:flex;flex-direction:column}
.filter-item label{font-weight:600;color:#FF6B35;margin-bottom:8px;font-size:.9rem}
.Select-control{border:2px solid #ffe8dd!important;border-radius:8px!important;transition:all .2s ease!important;background:white!important;min-height:42px!important}
.Select-control:hover{border-color:#FF8C42!important;box-shadow:0 0 0 3px rgba(255,107,53,.1)!important}
.Select-control.is-focused{border-color:#FF6B35!important;box-shadow:0 0 0 3px rgba(255,107,53,.15)!important}
.graphs-container{margin-bottom:25px}
.graph-card{background:linear-gradient(135deg,#ffffff 0%,#fffaf7 100%);border-radius:16px;padding:25px;box-shadow:0 4px 16px rgba(255,107,53,.1);border:2px solid #ffe8dd;transition:all .3s ease;position:relative;overflow:hidden}
.graph-card::before{content:'';position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,#FF6B35 0%,#FF8C42 50%,#FFB085 100%)}
.graph-card:hover{box-shadow:0 8px 24px rgba(255,107,53,.2);transform:translateY(-2px);border-color:#ffd4c4}
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
@media (max-width:1024px){.filters-container{grid-template-columns:1fr}.title-gradient{font-size:1.6rem}}
::-webkit-scrollbar{width:8px;height:8px}
::-webkit-scrollbar-track{background:#ffe8dd;border-radius:4px}
::-webkit-scrollbar-thumb{background:linear-gradient(135deg,#FF6B35,#FF8C42);border-radius:4px}
::-webkit-scrollbar-thumb:hover{background:linear-gradient(135deg,#FF8C42,#FFB085)}
</style></head><body>{%app_entry%}{%config%}{%scripts%}{%renderer%}</body></html>'''

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1("Dashboard de Monitoramento de Viagens", className="title-gradient"),
            html.Div("Acompanhe suas operacoes logisticas em tempo real", className="header-subtitle")
        ])
    ], className="title-container"),
    
    dcc.Interval(id="interval", interval=60000, n_intervals=0),
    
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
                dcc.DatePickerSingle(id="filtro-data-inicial", display_format="DD/MM/YYYY", placeholder="Selecione a data inicial", style={'width': '100%'})
            ], style={'flex': '1', 'minWidth': '250px'}),
            
            html.Div([
                html.Label("Data Final"),
                dcc.DatePickerSingle(id="filtro-data-final", display_format="DD/MM/YYYY", placeholder="Selecione a data final", style={'width': '100%'})
            ], style={'flex': '1', 'minWidth': '250px'}),
            
            html.Div([
                html.Label(" ", style={'visibility': 'hidden'}),
                html.Button("🔄 Limpar Filtros", id="btn-limpar-filtros", style={
                    'width': '100%', 'background': 'linear-gradient(135deg, #FF6B35, #FF8C42)', 'color': 'white',
                    'border': 'none', 'padding': '10px 20px', 'borderRadius': '8px', 'cursor': 'pointer',
                    'fontWeight': '600', 'fontSize': '0.9rem', 'boxShadow': '0 4px 12px rgba(255, 107, 53, 0.3)',
                    'transition': 'all 0.3s ease'
                })
            ], style={'flex': '1', 'minWidth': '250px'})
        ], style={'gridColumn': '1 / -1', 'display': 'flex', 'gap': '20px', 'justifyContent': 'center', 'marginTop': '15px'})
    ], className="filters-container"),
    
    html.Div([
        html.Div([dcc.Graph(id="grafico")], className="graph-card")
    ], className="graphs-container"),
    
    html.Div([
        html.Div([
            html.H3("Dados Detalhados", style={'display': 'inline-block', 'marginBottom': '0'}),
            html.Button("📥 Exportar CSV", id="btn-exportar", style={
                'float': 'right', 'background': 'linear-gradient(135deg, #28a745, #20c997)', 'color': 'white',
                'border': 'none', 'padding': '12px 24px', 'borderRadius': '8px', 'cursor': 'pointer',
                'fontWeight': '600', 'fontSize': '0.95rem', 'boxShadow': '0 4px 12px rgba(40, 167, 69, 0.3)',
                'transition': 'all 0.3s ease'
            }),
            dcc.Download(id="download-csv")
        ], style={'marginBottom': '20px', 'overflow': 'hidden'}),
        
        dash_table.DataTable(
            id="tabela", page_size=25, sort_action="native",
            style_table={"borderRadius": "6px", "height": "600px", "overflowY": "auto"},
            style_cell={"padding": "12px", "textAlign": "left", "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", "fontSize": "13px", "whiteSpace": "normal", "height": "auto"},
            style_header={"fontWeight": "700", "backgroundColor": "#FF6B35", "color": "white", "borderBottom": "2px solid #FF8C42", "fontSize": "14px", "padding": "15px", "textAlign": "center"},
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "#FFF5F0"},
                {"if": {"row_index": "even"}, "backgroundColor": "white"}
            ]
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
    
    def get_options(col):
        return [{"label": str(v), "value": v} for v in sorted(df[col].unique())] if col in df.columns else []
    
    return get_options("trip_number"), get_options("destination_station_code"), get_options("Status_da_Viagem")

@app.callback(
    Output("filtro-id", "value"),
    Output("filtro-destino", "value"),
    Output("filtro-status", "value"),
    Output("filtro-data-inicial", "date"),
    Output("filtro-data-final", "date"),
    Input("btn-limpar-filtros", "n_clicks"),
    prevent_initial_call=True
)
def limpar_filtros(n_clicks):
    return None, None, None, None, None

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
    df = carregar_dados().copy()
    
    if ids and "trip_number" in df.columns:
        df = df[df["trip_number"].isin(ids)]
    if destinos and "destination_station_code" in df.columns:
        df = df[df["destination_station_code"].isin(destinos)]
    if status and "Status_da_Viagem" in df.columns:
        df = df[df["Status_da_Viagem"].isin(status)]
    
    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"], format='%d/%m/%Y', errors="coerce")
        if data_inicial:
            df = df[df["Data"] >= pd.to_datetime(data_inicial)]
        if data_final:
            df = df[df["Data"] <= pd.to_datetime(data_final)]
    
    fig = criar_grafico(df)
    
    colunas_existentes = [c for c in COLUNAS_TABELA if c in df.columns]
    df_tabela = df[colunas_existentes] if colunas_existentes else df
    columns = [{"name": c, "id": c} for c in df_tabela.columns]
    
    return fig, columns, df_tabela.to_dict("records")

def criar_grafico(df):
    if "Data" not in df.columns:
        return go.Figure().add_annotation(text="Coluna Data nao encontrada")
    
    df_grafico = df.copy()
    df_grafico["Data"] = pd.to_datetime(df_grafico["Data"], format='%d/%m/%Y', errors="coerce")
    df_grafico = df_grafico.dropna(subset=["Data"])
    
    if df_grafico.empty or "Status_da_Viagem" not in df_grafico.columns:
        return go.Figure().add_annotation(text="Sem dados")
    
    contagem = df_grafico.groupby([df_grafico["Data"].dt.date, "Status_da_Viagem"]).size().reset_index()
    contagem.columns = ["Data", "Status", "Quantidade"]
    
    fig = px.bar(contagem, x="Data", y="Quantidade", color="Status", title="Viagens por Data e Status",
                 color_discrete_map=CORES_STATUS, barmode="group", text="Quantidade")
    fig.update_traces(textposition='outside', textfont_size=16)
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis_title="Data", yaxis_title="Quantidade de Viagens", legend_title="Status da Viagem",
        height=450,
        xaxis=dict(type='category', tickformat='%d/%m'),
        yaxis=dict(showticklabels=False, range=[0, contagem['Quantidade'].max() * 1.15])
    )
    return fig

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
    
    df = carregar_dados().copy()
    
    if ids and "trip_number" in df.columns:
        df = df[df["trip_number"].isin(ids)]
    if destinos and "destination_station_code" in df.columns:
        df = df[df["destination_station_code"].isin(destinos)]
    if status and "Status_da_Viagem" in df.columns:
        df = df[df["Status_da_Viagem"].isin(status)]
    
    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"], format='%d/%m/%Y', errors="coerce")
        if data_inicial:
            df = df[df["Data"] >= pd.to_datetime(data_inicial)]
        if data_final:
            df = df[df["Data"] <= pd.to_datetime(data_final)]
    
    colunas_existentes = [c for c in COLUNAS_TABELA if c in df.columns]
    df_export = df[colunas_existentes] if colunas_existentes else df
    
    return dcc.send_data_frame(df_export.to_csv, "dados_viagens.csv", index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    print("\n" + "="*70)
    print("Dashboard rodando em:")
    print("  Local:  http://127.0.0.1:8051/")
    app.run(debug=True, host='0.0.0.0', port=8051)
