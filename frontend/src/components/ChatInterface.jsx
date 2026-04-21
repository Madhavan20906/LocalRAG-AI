import { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';
import MessageBubble from './MessageBubble';

export default function ChatInterface({ isDocumentReady }) {
  const [messages, setMessages] = useState([
    { role: 'ai', content: 'Hello! I am your Local RAG Assistant. Upload a document to get started, and I can answer questions about it based on the extracted context.', sources: [] }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMessage.content, top_k: 3 }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch response');
      }

      const data = await response.json();
      
      setMessages((prev) => [...prev, {
        role: 'ai',
        content: data.answer,
        sources: data.sources || []
      }]);
    } catch (error) {
      setMessages((prev) => [...prev, {
        role: 'ai',
        content: `Error: ${error.message}. Please ensure the backend is running.`,
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <>
      <div className="messages-container">
        {messages.map((msg, index) => (
          <MessageBubble key={index} message={msg} />
        ))}
        {isLoading && (
          <div className="message-wrapper ai">
            <div className="message-bubble" style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
              <Loader2 className="brand-icon" size={16} /> Thinking...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <div className="input-container">
          <input
            type="text"
            className="chat-input"
            placeholder={isDocumentReady ? "Ask a question about your document..." : "Upload a PDF first to ask questions..."}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading || (!isDocumentReady && messages.length > 1)}
          />
          <button 
            className="send-button"
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </>
  );
}
