import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export interface TripData {
  trip_number: string;
  Status_da_Viagem: string;
  'ETA Planejado': string;
  'Ultima localização': string;
  'Previsão de chegada': string;
  Ocorrencia: string;
  Data: string;
  destination_station_code: string;
}

export interface Filters {
  trip_numbers: string[];
  destinations: string[];
  status: string[];
}

export interface Stats {
  status_counts: Record<string, number>;
  timeline: Array<{
    Data: string;
    Status: string;
    Quantidade: number;
  }>;
}

export const api = {
  getData: async (params?: {
    trip_numbers?: string[];
    destinations?: string[];
    status?: string[];
    start_date?: string;
    end_date?: string;
  }): Promise<TripData[]> => {
    const queryParams = new URLSearchParams();
    if (params?.trip_numbers?.length) queryParams.append('trip_numbers', params.trip_numbers.join(','));
    if (params?.destinations?.length) queryParams.append('destinations', params.destinations.join(','));
    if (params?.status?.length) queryParams.append('status', params.status.join(','));
    if (params?.start_date) queryParams.append('start_date', params.start_date);
    if (params?.end_date) queryParams.append('end_date', params.end_date);
    
    const response = await axios.get(`${API_URL}/data?${queryParams}`);
    return response.data;
  },

  getFilters: async (): Promise<Filters> => {
    const response = await axios.get(`${API_URL}/filters`);
    return response.data;
  },

  getStats: async (): Promise<Stats> => {
    const response = await axios.get(`${API_URL}/stats`);
    return response.data;
  }
};
