import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Enable CORS for frontend
  app.enableCors({
    origin: ['http://localhost:5173', 'http://localhost:3000'],
    credentials: true,
  });

  const port = process.env.GATEWAY_PORT || 3001;
  await app.listen(port);
  console.log(`🏥 MedAssist Gateway running on http://localhost:${port}`);
}

bootstrap();
