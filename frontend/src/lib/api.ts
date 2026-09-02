import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface QueryResponse {
  request_id: string;
  timestamp: string;
  final_answer: string;
  contributing_agents: string[];
  verification_verdict: string;
  final_confidence: {
    level: string;
    score: number;
    basis: string;
  };
  citations: string[];
  caveats: string[];
  unresolved_conflicts: string[];
}

export const submitQuery = async (query: string): Promise<QueryResponse> => {
  const response = await apiClient.post('/api/v1/query', {
    user_query: query,
  });
  return response.data;
};
