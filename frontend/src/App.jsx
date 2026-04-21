import { useState } from 'react';
import { Bot } from 'lucide-react';
import FileUpload from './components/FileUpload';
import ChatInterface from './components/ChatInterface';

function App() {
  const [documentUploaded, setDocumentUploaded] = useState(false);

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="brand">
          <Bot className="brand-icon" size={28} />
          <h1>Local RAG AI</h1>
        </div>
      </header>
      
      <main className="main-layout">
        <aside className="sidebar">
          <FileUpload onUploadSuccess={() => setDocumentUploaded(true)} />
        </aside>
        
        <section className="chat-area">
          <ChatInterface isDocumentReady={documentUploaded} />
        </section>
      </main>
    </div>
  );
}

export default App;
