import { Module } from '@nestjs/common';
import { ChatController } from './chat.controller';
import { AiServiceProxy } from './ai-service.proxy';

@Module({
  controllers: [ChatController],
  providers: [AiServiceProxy],
})
export class AppModule {}
