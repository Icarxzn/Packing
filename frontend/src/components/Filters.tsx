import { Card, MultiSelect, MultiSelectItem, DatePicker, Button } from '@tremor/react';

interface FiltersProps {
  filters: {
    trip_numbers: string[];
    destinations: string[];
    status: string[];
  };
  selectedFilters: {
    trip_numbers: string[];
    destinations: string[];
    status: string[];
    start_date?: Date;
    end_date?: Date;
  };
  onFilterChange: (filters: {
    trip_numbers: string[];
    destinations: string[];
    status: string[];
    start_date?: Date;
    end_date?: Date;
  }) => void;
  onClear: () => void;
}

export default function Filters({ filters, selectedFilters, onFilterChange, onClear }: FiltersProps) {
  return (
    <Card className="glass-effect rounded-2xl border-0 p-6 shadow-xl">
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold gradient-text">Filtros</h3>
          <Button
            onClick={onClear}
            size="sm"
            variant="secondary"
            className="bg-gradient-to-r from-slate-100 to-slate-200 hover:from-slate-200 hover:to-slate-300 border-0 text-slate-700 font-medium"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Limpar
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="space-y-2">
            <label className="block text-sm font-semibold text-slate-700">
              ID (LT)
            </label>
            <MultiSelect
              value={selectedFilters.trip_numbers}
              onValueChange={(value: string[]) => onFilterChange({ ...selectedFilters, trip_numbers: value })}
              placeholder="Selecione..."
              className="rounded-xl"
            >
              {filters.trip_numbers.map((id) => (
                <MultiSelectItem key={id} value={id}>
                  {id}
                </MultiSelectItem>
              ))}
            </MultiSelect>
          </div>

          <div className="space-y-2">
            <label className="block text-sm font-semibold text-slate-700">
              Destino
            </label>
            <MultiSelect
              value={selectedFilters.destinations}
              onValueChange={(value: string[]) => onFilterChange({ ...selectedFilters, destinations: value })}
              placeholder="Selecione..."
              className="rounded-xl"
            >
              {filters.destinations.map((dest) => (
                <MultiSelectItem key={dest} value={dest}>
                  {dest}
                </MultiSelectItem>
              ))}
            </MultiSelect>
          </div>

          <div className="space-y-2">
            <label className="block text-sm font-semibold text-slate-700">
              Status
            </label>
            <MultiSelect
              value={selectedFilters.status}
              onValueChange={(value: string[]) => onFilterChange({ ...selectedFilters, status: value })}
              placeholder="Selecione..."
              className="rounded-xl"
            >
              {filters.status.map((s) => (
                <MultiSelectItem key={s} value={s}>
                  {s}
                </MultiSelectItem>
              ))}
            </MultiSelect>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="block text-sm font-semibold text-slate-700">
              Data Inicial
            </label>
            <DatePicker
              value={selectedFilters.start_date}
              onValueChange={(date: Date | undefined) => onFilterChange({ ...selectedFilters, start_date: date })}
              placeholder="Selecione..."
              className="rounded-xl"
            />
          </div>

          <div className="space-y-2">
            <label className="block text-sm font-semibold text-slate-700">
              Data Final
            </label>
            <DatePicker
              value={selectedFilters.end_date}
              onValueChange={(date: Date | undefined) => onFilterChange({ ...selectedFilters, end_date: date })}
              placeholder="Selecione..."
              className="rounded-xl"
            />
          </div>
        </div>
      </div>
    </Card>
  );
}
