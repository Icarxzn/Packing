import { useEffect, useState } from 'react';
import { Card, Title, BarChart, DonutChart, Grid, Metric, Text, Badge } from '@tremor/react';
import { api, TripData, Filters as FilterData, Stats } from '../services/api';
import Filters from './Filters';
import DataTable from './DataTable';
import { format } from 'date-fns';

export default function Dashboard() {
  const [data, setData] = useState<TripData[]>([]);
  const [filters, setFilters] = useState<FilterData>({ trip_numbers: [], destinations: [], status: [] });
  const [stats, setStats] = useState<Stats | null>(null);
  const [selectedFilters, setSelectedFilters] = useState({
    trip_numbers: [] as string[],
    destinations: [] as string[],
    status: [] as string[],
    start_date: undefined as Date | undefined,
    end_date: undefined as Date | undefined,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFilters();
    loadData();
    loadStats();
    
    const interval = setInterval(() => {
      loadData();
      loadStats();
    }, 60000);
    
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    loadData();
  }, [selectedFilters]);

  const loadFilters = async () => {
    try {
      const filterData = await api.getFilters();
      setFilters(filterData);
    } catch (error) {
      console.error('Erro ao carregar filtros:', error);
    }
  };

  const loadData = async () => {
    try {
      setLoading(true);
      const params = {
        trip_numbers: selectedFilters.trip_numbers,
        destinations: selectedFilters.destinations,
        status: selectedFilters.status,
        start_date: selectedFilters.start_date ? format(selectedFilters.start_date, 'yyyy-MM-dd') : undefined,
        end_date: selectedFilters.end_date ? format(selectedFilters.end_date, 'yyyy-MM-dd') : undefined,
      };
      const tripData = await api.getData(params);
      setData(tripData);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const statsData = await api.getStats();
      setStats(statsData);
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error);
    }
  };

  const handleClearFilters = () => {
    setSelectedFilters({
      trip_numbers: [],
      destinations: [],
      status: [],
      start_date: undefined,
      end_date: undefined,
    });
  };

  const handleExport = () => {
    const csv = [
      ['Trip Number', 'Status', 'ETA Planejado', 'Última Localização', 'Previsão de Chegada', 'Ocorrência'],
      ...data.map((row: TripData) => [
        row.trip_number,
        row.Status_da_Viagem,
        row['ETA Planejado'],
        row['Ultima localização'],
        row['Previsão de chegada'],
        row.Ocorrencia
      ])
    ].map((row: string[]) => row.join(',')).join('\n');

    const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'dados_viagens.csv';
    link.click();
  };

  const statusData = stats?.status_counts
    ? Object.entries(stats.status_counts).map(([name, value]) => ({ name, value }))
    : [];

  const timelineData = stats?.timeline || [];

  const emTransito = data.filter((d: TripData) => 
    d.Status_da_Viagem === 'Em trânsito' || d.Status_da_Viagem === 'Em transito'
  ).length;
  
  const paradas = data.filter((d: TripData) => d.Status_da_Viagem === 'Parado').length;
  const finalizadas = data.filter((d: TripData) => d.Status_da_Viagem === 'Finalizado').length;

  return (
    <div className="min-h-screen p-4 md:p-8 animate-fade-in">
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* Header Premium */}
        <div className="glass-effect rounded-3xl p-8 md:p-10 animate-slide-up shadow-2xl">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <h1 className="text-4xl md:text-5xl font-bold gradient-text mb-2">
                Dashboard de Monitoramento
              </h1>
              <p className="text-slate-600 text-lg">
                Acompanhe suas operações logísticas em tempo real
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Badge size="xl" className="bg-gradient-to-r from-green-500 to-emerald-500 text-white border-0 px-4 py-2">
                <span className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-white rounded-full animate-pulse"></span>
                  Online
                </span>
              </Badge>
            </div>
          </div>
        </div>

        {/* Filtros */}
        <div className="animate-slide-up" style={{ animationDelay: '0.1s' }}>
          <Filters
            filters={filters}
            selectedFilters={selectedFilters}
            onFilterChange={setSelectedFilters}
            onClear={handleClearFilters}
          />
        </div>

        {/* Cards de Métricas */}
        <Grid numItems={1} numItemsSm={2} numItemsLg={4} className="gap-6 animate-scale-in" style={{ animationDelay: '0.2s' }}>
          <Card className="glass-effect rounded-2xl border-0 card-hover">
            <div className="flex items-center justify-between">
              <div>
                <Text className="text-slate-600 font-medium">Total de Viagens</Text>
                <Metric className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
                  {data.length}
                </Metric>
              </div>
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center shadow-lg">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
            </div>
          </Card>
          
          <Card className="glass-effect rounded-2xl border-0 card-hover">
            <div className="flex items-center justify-between">
              <div>
                <Text className="text-slate-600 font-medium">Em Trânsito</Text>
                <Metric className="text-4xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                  {emTransito}
                </Metric>
              </div>
              <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center shadow-lg">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
            </div>
          </Card>
          
          <Card className="glass-effect rounded-2xl border-0 card-hover">
            <div className="flex items-center justify-between">
              <div>
                <Text className="text-slate-600 font-medium">Paradas</Text>
                <Metric className="text-4xl font-bold bg-gradient-to-r from-red-600 to-rose-600 bg-clip-text text-transparent">
                  {paradas}
                </Metric>
              </div>
              <div className="w-16 h-16 bg-gradient-to-br from-red-500 to-rose-500 rounded-2xl flex items-center justify-center shadow-lg">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
            </div>
          </Card>

          <Card className="glass-effect rounded-2xl border-0 card-hover">
            <div className="flex items-center justify-between">
              <div>
                <Text className="text-slate-600 font-medium">Finalizadas</Text>
                <Metric className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
                  {finalizadas}
                </Metric>
              </div>
              <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-indigo-500 rounded-2xl flex items-center justify-center shadow-lg">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </Card>
        </Grid>

        {/* Gráficos */}
        <Grid numItems={1} numItemsLg={2} className="gap-6 animate-scale-in" style={{ animationDelay: '0.3s' }}>
          <Card className="glass-effect rounded-2xl border-0 p-6 card-hover">
            <Title className="text-2xl font-bold gradient-text mb-6">Distribuição por Status</Title>
            <DonutChart
              data={statusData}
              category="value"
              index="name"
              colors={['red', 'green', 'gray', 'yellow', 'blue']}
              className="h-72"
              showAnimation={true}
            />
          </Card>

          <Card className="glass-effect rounded-2xl border-0 p-6 card-hover">
            <Title className="text-2xl font-bold gradient-text mb-6">Timeline de Viagens</Title>
            <BarChart
              data={timelineData}
              index="Data"
              categories={['Quantidade']}
              colors={['blue']}
              className="h-72"
              showAnimation={true}
            />
          </Card>
        </Grid>

        {/* Tabela */}
        <div className="animate-scale-in" style={{ animationDelay: '0.4s' }}>
          <DataTable data={data} onExport={handleExport} loading={loading} />
        </div>

      </div>
    </div>
  );
}
