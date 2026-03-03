import type { ChatMessage } from '../types/chat';
import { useTextToSpeech } from '../hooks/useTextToSpeech';

interface MessageBubbleProps {
  message: ChatMessage;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const { isSpeaking, speak, stop, isSupported } = useTextToSpeech();
  const isUser = message.role === 'user';

  // Simple markdown-like rendering for bold and newlines
  const formatContent = (text: string) => {
    return text.split('\n').map((line, i) => {
      const formatted = line.replace(
        /\*\*(.+?)\*\*/g,
        '<strong>$1</strong>'
      );
      return (
        <span key={i}>
          {i > 0 && <br />}
          <span dangerouslySetInnerHTML={{ __html: formatted }} />
        </span>
      );
    });
  };

  return (
    <div
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 animate-in`}
    >
      <div
        className={`max-w-[75%] rounded-2xl px-5 py-3 shadow-sm ${
          isUser
            ? 'bg-sky-500 text-white rounded-br-md'
            : 'bg-white text-slate-800 rounded-bl-md border border-slate-100'
        }`}
      >
        {/* Intent badge for non-ANSWER responses */}
        {!isUser && message.intent && message.intent !== 'ANSWER' && (
          <span
            className={`inline-block text-xs font-semibold px-2 py-0.5 rounded-full mb-2 ${
              message.intent === 'ESCALATE'
                ? 'bg-red-100 text-red-700'
                : 'bg-amber-100 text-amber-700'
            }`}
          >
            {message.intent === 'ESCALATE' ? '🚨 Emergency' : '❓ Clarification'}
          </span>
        )}

        {/* Loading state */}
        {message.isLoading ? (
          <div className="flex items-center gap-1.5 py-1">
            <span className="typing-dot w-2 h-2 bg-slate-400 rounded-full" />
            <span className="typing-dot w-2 h-2 bg-slate-400 rounded-full" />
            <span className="typing-dot w-2 h-2 bg-slate-400 rounded-full" />
          </div>
        ) : (
          <div className="text-sm leading-relaxed">
            {formatContent(message.content)}
          </div>
        )}

        {/* Sources */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="mt-3 pt-2 border-t border-slate-100">
            <p className="text-xs font-medium text-slate-500 mb-1">📚 Sources:</p>
            {message.sources.map((source, i) => (
              <span
                key={i}
                className="inline-block text-xs bg-sky-50 text-sky-700 px-2 py-0.5 rounded-full mr-1 mb-1"
              >
                {source.document} (p.{source.page})
              </span>
            ))}
          </div>
        )}

        {/* Footer: timestamp + TTS */}
        <div
          className={`flex items-center gap-2 mt-2 text-xs ${
            isUser ? 'text-sky-100' : 'text-slate-400'
          }`}
        >
          <span>
            {message.timestamp.toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </span>

          {!isUser && isSupported && !message.isLoading && (
            <button
              onClick={() => (isSpeaking ? stop() : speak(message.content))}
              className="hover:text-sky-500 transition-colors cursor-pointer"
              title={isSpeaking ? 'Stop speaking' : 'Read aloud'}
            >
              {isSpeaking ? '🔇' : '🔊'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
