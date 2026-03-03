import { useEffect } from 'react';
import { useSpeechToText } from '../hooks/useSpeechToText';

interface VoiceInputProps {
  onTranscript: (text: string) => void;
}

export function VoiceInput({ onTranscript }: VoiceInputProps) {
  const { isListening, transcript, startListening, stopListening, isSupported } =
    useSpeechToText();

  useEffect(() => {
    if (!isListening && transcript) {
      onTranscript(transcript);
    }
  }, [isListening, transcript, onTranscript]);

  if (!isSupported) return null;

  return (
    <button
      onClick={isListening ? stopListening : startListening}
      className={`relative p-2.5 rounded-full transition-all cursor-pointer ${
        isListening
          ? 'bg-red-500 text-white mic-pulse'
          : 'bg-slate-100 text-slate-500 hover:bg-slate-200 hover:text-slate-700'
      }`}
      title={isListening ? 'Stop recording' : 'Voice input'}
      type="button"
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
        <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
        <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
        <line x1="12" x2="12" y1="19" y2="22" />
      </svg>
    </button>
  );
}
