import { Controller, Post, Get, Body, HttpCode } from '@nestjs/common';
import { AiServiceProxy } from './ai-service.proxy';

interface ChatMessageDto {
  role: string;
  content: string;
}

interface QueryDto {
  question: string;
  chat_history?: ChatMessageDto[];
}

@Controller('api')
export class ChatController {
  constructor(private readonly aiService: AiServiceProxy) {}

  @Get('health')
  async health() {
    return this.aiService.healthCheck();
  }

  @Post('query')
  @HttpCode(200)
  async query(@Body() body: QueryDto) {
    const { question, chat_history = [] } = body;
    return this.aiService.query(question, chat_history);
  }

  @Post('ingest')
  @HttpCode(200)
  async ingest() {
    return this.aiService.ingestDocuments();
  }
}
