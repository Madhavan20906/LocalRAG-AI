import { FileText } from 'lucide-react';

export default function MessageBubble({ message }) {
  const { role, content, sources } = message;

  return (
    <div className={`message-wrapper ${role}`}>
      <div className="message-bubble">
        <div style={{ whiteSpace: 'pre-wrap' }}>{content}</div>
        
        {sources && sources.length > 0 && (
          <div className="sources-container">
            {sources.map((source, idx) => (
              <div 
                key={idx} 
                className="source-pill" 
                title={source.text} // Show chunk text on hover
              >
                <FileText size={12} />
                <span>{source.metadata.filename}</span>
                <span style={{ opacity: 0.5, fontSize: '0.65rem' }}>({(source.score).toFixed(2)})</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
