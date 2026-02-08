import { Card, Table, TableHead, TableRow, TableHeaderCell, TableBody, TableCell, Button, Badge } from '@tremor/react';
import { TripData } from '../services/api';

interface DataTableProps {
  data: TripData[];
  onExport: () => void;
  loading?: boolean;
}

const STATUS_COLORS: Record<string, 'red' | 'green' | 'gray' | 'yellow'> = {
  'Parado': 'red',
  'Em trânsito': 'green',
  'Em transito': 'green',
  'Finalizado': 'gray',
  'Cancelado': 'yellow'
};

export default function DataTable({ data, onExport, loading }: DataTableProps) {
  return (
    <Card className="glass-effect rounded-2xl border-0 p-6 shadow-xl">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h3 className="text-2xl font-bold gradient-text">Dados Detalhados</h3>
          <p className="text-slate-600 text-sm mt-1">{data.length} viagens encontradas</p>
        </div>
        <Button
          onClick={onExport}
          className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 border-0 text-white font-medium shadow-lg"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Exportar CSV
        </Button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      ) : (
        <div className="overflow-x-auto rounded-xl">
          <Table>
            <TableHead>
              <TableRow className="bg-gradient-to-r from-blue-600 to-indigo-600">
                <TableHeaderCell className="text-white font-bold">Trip Number</TableHeaderCell>
                <TableHeaderCell className="text-white font-bold">Status</TableHeaderCell>
                <TableHeaderCell className="text-white font-bold">ETA Planejado</TableHeaderCell>
                <TableHeaderCell className="text-white font-bold">Última Localização</TableHeaderCell>
                <TableHeaderCell className="text-white font-bold">Previsão de Chegada</TableHeaderCell>
                <TableHeaderCell className="text-white font-bold">Ocorrência</TableHeaderCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((row, idx) => (
                <TableRow 
                  key={idx} 
                  className="hover:bg-blue-50/50 transition-colors duration-200"
                >
                  <TableCell className="font-semibold text-slate-900">{row.trip_number}</TableCell>
                  <TableCell>
                    <Badge 
                      color={STATUS_COLORS[row.Status_da_Viagem] || 'gray'}
                      size="sm"
                      className="font-medium"
                    >
                      {row.Status_da_Viagem}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-slate-700">{row['ETA Planejado']}</TableCell>
                  <TableCell className="text-slate-700">{row['Ultima localização']}</TableCell>
                  <TableCell className="text-slate-700">{row['Previsão de chegada']}</TableCell>
                  <TableCell className="text-slate-700">{row.Ocorrencia}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </Card>
  );
}
