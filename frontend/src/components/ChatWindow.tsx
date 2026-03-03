import { useState, useRef, useEffect, useCallback } from 'react';
import type { ChatMessage } from '../types/chat';
import { sendQuery } from '../services/api';
import { MessageBubble } from './MessageBubble';
import { VoiceInput } from './VoiceInput';

const WELCOME_MESSAGE: ChatMessage = {
  id: 'welcome',
  role: 'assistant',
  content:
    '👋 Hello! I\'m **MedAssist AI**, your healthcare information assistant.\n\n' +
    'I can answer health-related questions using trusted medical sources like NHS, WHO, and CDC guidelines.\n\n' +
    'You can type your question or use the 🎤 microphone button to speak.\n\n' +
    '⚕️ *Remember: I provide information only — always consult your healthcare provider for personal medical advice.*',
  timestamp: new Date(),
};

export function ChatWindow() {
  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME_MESSAGE]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSubmit = useCallback(
    async (text?: string) => {
      const question = (text || input).trim();
      if (!question || isLoading) return;

      // Add user message
      const userMessage: ChatMessage = {
        id: Date.now().toString(),
        role: 'user',
        content: question,
        timestamp: new Date(),
      };

      // Add loading placeholder
      const loadingMessage: ChatMessage = {
        id: `loading-${Date.now()}`,
        role: 'assistant',
        content: '',
        timestamp: new Date(),
        isLoading: true,
      };

      setMessages((prev) => [...prev, userMessage, loadingMessage]);
      setInput('');
      setIsLoading(true);

      try {
        // Build chat history (excluding welcome and loading messages)
        const chatHistory = messages
          .filter((m) => m.id !== 'welcome' && !m.isLoading)
          .map((m) => ({ role: m.role, content: m.content }));

        const response = await sendQuery({
          question,
          chat_history: chatHistory,
        });

        const assistantMessage: ChatMessage = {
          id: `response-${Date.now()}`,
          role: 'assistant',
          content: response.answer,
          timestamp: new Date(),
          intent: response.intent as ChatMessage['intent'],
          sources: response.sources,
        };

        // Replace loading message with actual response
        setMessages((prev) =>
          prev.filter((m) => !m.isLoading).concat(assistantMessage)
        );
      } catch (error) {
        const errorMessage: ChatMessage = {
          id: `error-${Date.now()}`,
          role: 'assistant',
          content:
            '❌ Sorry, I encountered an error. Please make sure the backend service is running and try again.',
          timestamp: new Date(),
        };

        setMessages((prev) =>
          prev.filter((m) => !m.isLoading).concat(errorMessage)
        );
      } finally {
        setIsLoading(false);
        inputRef.current?.focus();
      }
    },
    [input, isLoading, messages]
  );

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleVoiceTranscript = useCallback(
    (text: string) => {
      if (text.trim()) {
        setInput(text);
        // Auto-submit voice input after a brief delay
        setTimeout(() => handleSubmit(text), 300);
      }
    },
    [handleSubmit]
  );

  return (
    <div className="flex flex-col h-full max-w-3xl mx-auto w-full">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-1">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="border-t border-slate-200 bg-white p-4">
        <div className="flex items-end gap-2 max-w-3xl mx-auto">
          <VoiceInput onTranscript={handleVoiceTranscript} />

          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a health question..."
              className="w-full resize-none rounded-xl border border-slate-200 px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent placeholder:text-slate-400 max-h-32"
              rows={1}
              disabled={isLoading}
              onInput={(e) => {
                const target = e.target as HTMLTextAreaElement;
                target.style.height = 'auto';
                target.style.height = Math.min(target.scrollHeight, 128) + 'px';
              }}
            />
          </div>

          <button
            onClick={() => handleSubmit()}
            disabled={isLoading || !input.trim()}
            className="p-2.5 rounded-xl bg-sky-500 text-white hover:bg-sky-600 disabled:opacity-40 disabled:cursor-not-allowed transition-colors cursor-pointer"
            title="Send message"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="m22 2-7 20-4-9-9-4Z" />
              <path d="M22 2 11 13" />
            </svg>
          </button>
        </div>

        <p className="text-center text-xs text-slate-400 mt-2">
          MedAssist AI provides information only — not medical advice. Always consult a healthcare professional.
        </p>
      </div>
    </div>
  );
}
