import { useState, useEffect } from 'react';
import { ChatWindow } from './components/ChatWindow';
import { checkHealth } from './services/api';

function App() {
  const [status, setStatus] = useState<'connecting' | 'connected' | 'disconnected'>('connecting');
  const [docCount, setDocCount] = useState(0);

  useEffect(() => {
    const check = async () => {
      try {
        const health = await checkHealth();
        setStatus('connected');
        setDocCount(health.documents_indexed);
      } catch {
        setStatus('disconnected');
      }
    };
    check();
    const interval = setInterval(check, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 px-6 py-3 shadow-sm">
        <div className="max-w-3xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-sky-500 rounded-xl flex items-center justify-center text-white font-bold text-lg">
              M
            </div>
            <div>
              <h1 className="text-lg font-bold text-slate-800">MedAssist AI</h1>
              <p className="text-xs text-slate-500">Healthcare Information Assistant</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {docCount > 0 && (
              <span className="text-xs text-slate-500 bg-slate-50 px-2 py-1 rounded-full">
                📚 {docCount} chunks indexed
              </span>
            )}
            <div className="flex items-center gap-1.5">
              <span
                className={`w-2 h-2 rounded-full ${
                  status === 'connected'
                    ? 'bg-emerald-400'
                    : status === 'connecting'
                    ? 'bg-amber-400 animate-pulse'
                    : 'bg-red-400'
                }`}
              />
              <span className="text-xs text-slate-500 capitalize">{status}</span>
            </div>
          </div>
        </div>
      </header>

      {/* Disconnected warning */}
      {status === 'disconnected' && (
        <div className="bg-amber-50 border-b border-amber-200 px-6 py-2 text-center">
          <p className="text-sm text-amber-700">
            ⚠️ Backend service is not running. Start the FastAPI server:{' '}
            <code className="bg-amber-100 px-1.5 py-0.5 rounded text-xs">
              cd backend/ai-service && python main.py
            </code>
          </p>
        </div>
      )}

      {/* Chat area */}
      <main className="flex-1 overflow-hidden bg-gradient-to-b from-sky-50 to-white">
        <ChatWindow />
      </main>
    </div>
  );
}

export default App;
