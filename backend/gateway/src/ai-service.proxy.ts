import { Injectable, HttpException, HttpStatus } from '@nestjs/common';
import axios, { AxiosInstance } from 'axios';

@Injectable()
export class AiServiceProxy {
  private readonly client: AxiosInstance;

  constructor() {
    const aiServiceUrl = process.env.AI_SERVICE_URL || 'http://localhost:8000';

    this.client = axios.create({
      baseURL: aiServiceUrl,
      timeout: 30000, // 30s timeout for LLM calls
      headers: { 'Content-Type': 'application/json' },
    });
  }

  async query(question: string, chatHistory: { role: string; content: string }[]) {
    try {
      const response = await this.client.post('/query', {
        question,
        chat_history: chatHistory,
      });
      return response.data;
    } catch (error: any) {
      const status = error.response?.status || HttpStatus.SERVICE_UNAVAILABLE;
      const message = error.response?.data?.detail || 'AI service unavailable';
      throw new HttpException(message, status);
    }
  }

  async healthCheck() {
    try {
      const response = await this.client.get('/health');
      return response.data;
    } catch {
      throw new HttpException('AI service unavailable', HttpStatus.SERVICE_UNAVAILABLE);
    }
  }

  async ingestDocuments() {
    try {
      const response = await this.client.post('/ingest');
      return response.data;
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Ingestion failed';
      throw new HttpException(message, HttpStatus.INTERNAL_SERVER_ERROR);
    }
  }
}
