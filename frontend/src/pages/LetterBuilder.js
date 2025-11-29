import React, { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const LetterBuilder = () => {
  const [fields, setFields] = useState({
    date: new Date().toISOString().split('T')[0],
    recipient_name: '',
    account_number: '',
    consumer_name: '',
    consumer_address: ''
  });
  const [generatedLetter, setGeneratedLetter] = useState(null);

  const handleGenerate = async () => {
    try {
      const response = await axios.post(`${API_URL}/api/writer/generate`, {
        template_id: 'debt_validation_v1',
        template_version: '1.0.0',
        fields,
        tone: 'formal',
        user_id: 'test_user_001',
        trace_id: `letter_${Date.now()}`
      });
      setGeneratedLetter(response.data);
    } catch (error) {
      console.error('Generation error:', error);
    }
  };

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Generate Debt Validation Letter</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="space-y-4">
            <input
              type="text"
              placeholder="Recipient Name"
              value={fields.recipient_name}
              onChange={(e) => setFields({...fields, recipient_name: e.target.value})}
              className="w-full px-4 py-2 border rounded"
              data-testid="input-recipient"
            />
            <input
              type="text"
              placeholder="Account Number"
              value={fields.account_number}
              onChange={(e) => setFields({...fields, account_number: e.target.value})}
              className="w-full px-4 py-2 border rounded"
              data-testid="input-account"
            />
            <input
              type="text"
              placeholder="Your Name"
              value={fields.consumer_name}
              onChange={(e) => setFields({...fields, consumer_name: e.target.value})}
              className="w-full px-4 py-2 border rounded"
              data-testid="input-consumer-name"
            />
            <textarea
              placeholder="Your Address"
              value={fields.consumer_address}
              onChange={(e) => setFields({...fields, consumer_address: e.target.value})}
              className="w-full px-4 py-2 border rounded"
              rows={3}
              data-testid="input-address"
            />
            <button
              onClick={handleGenerate}
              className="w-full px-6 py-3 bg-primary-600 text-white rounded-lg"
              data-testid="generate-button"
            >
              Generate Letter
            </button>
          </div>
          
          <div className="bg-white rounded-lg p-6 border">
            {generatedLetter ? (
              <div>
                <h3 className="font-semibold mb-4">Preview</h3>
                <div dangerouslySetInnerHTML={{ __html: generatedLetter.html_preview }} />
                <div className="mt-4 text-sm text-neutral-600">
                  Hash: {generatedLetter.hash.substring(0, 16)}...
                </div>
              </div>
            ) : (
              <div className="text-neutral-500">Letter preview will appear here</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LetterBuilder;
