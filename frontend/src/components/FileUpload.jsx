import { useState, useRef } from 'react';
import { UploadCloud, FileText, CheckCircle } from 'lucide-react';

export default function FileUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError(null);
      setIsSuccess(false);
    } else {
      setError('Please select a valid PDF file.');
      setFile(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      setIsSuccess(true);
      onUploadSuccess();
    } catch (err) {
      setError(err.message || 'Error uploading file');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="upload-section">
      <h2>Document Context</h2>
      
      <div 
        className="dropzone"
        onClick={() => fileInputRef.current?.click()}
      >
        <UploadCloud className="drop-icon" />
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Click or drag PDF to upload
        </p>
        <input 
          type="file" 
          accept=".pdf" 
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handleFileChange}
        />
      </div>

      {file && (
        <div className="file-info">
          <FileText size={20} color="var(--accent-color)" />
          <span style={{ fontSize: '0.9rem', flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
            {file.name}
          </span>
          {isSuccess && <CheckCircle size={18} color="#2ea043" />}
        </div>
      )}

      {error && (
        <div style={{ color: '#f85149', fontSize: '0.85rem', marginTop: '0.5rem' }}>
          {error}
        </div>
      )}

      <button 
        className="upload-button"
        disabled={!file || isUploading || isSuccess}
        onClick={handleUpload}
      >
        {isUploading ? 'Extracting & Embedding...' : isSuccess ? 'Ready to Query' : 'Process Document'}
      </button>
    </div>
  );
}
