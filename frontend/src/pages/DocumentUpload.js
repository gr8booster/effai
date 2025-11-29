import React, { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const DocumentUpload = () => {
  const [uploading, setUploading] = useState(false);
  const [file, setFile] = useState(null);

  const handleFileSelect = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', 'test_user_001');
    formData.append('trace_id', `upload_${Date.now()}`);

    try {
      const response = await axios.post(`${API_URL}/api/intake/upload`, formData);
      alert('Document uploaded and processed!');
    } catch (error) {
      console.error('Upload error:', error);
      alert('Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Upload Documents</h1>
        
        <div className="bg-white rounded-lg p-8 border-2 border-dashed border-neutral-300">
          <input type="file" onChange={handleFileSelect} data-testid="file-input" />
          <button 
            onClick={handleUpload} 
            disabled={!file || uploading}
            className="mt-4 px-6 py-3 bg-primary-600 text-white rounded-lg disabled:opacity-50"
            data-testid="upload-button"
          >
            {uploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default DocumentUpload;
