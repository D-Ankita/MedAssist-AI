export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  intent?: 'ANSWER' | 'CLARIFY' | 'ESCALATE';
  sources?: Source[];
  isLoading?: boolean;
}

export interface Source {
  document: string;
  page: number;
  relevance: number;
}

export interface QueryRequest {
  question: string;
  chat_history: { role: string; content: string }[];
}

export interface QueryResponse {
  intent: string;
  answer: string;
  sources: Source[];
  chunks_retrieved: number;
  relevance_scores: number[];
}

export interface HealthStatus {
  status: string;
  service: string;
  documents_indexed: number;
}
