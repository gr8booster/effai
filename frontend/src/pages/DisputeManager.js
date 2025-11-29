import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Disclaimer from '../components/Disclaimer';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const DisputeManager = () => {
  const navigate = useNavigate();
  const [disputeForm, setDisputeForm] = useState({
    bureau: 'Equifax',
    disputed_item: '',
    account_number: '',
    dispute_reason: '',
    consumer_name: '',
    consumer_address: ''
  });
  const [generatedLetter, setGeneratedLetter] = useState(null);
  const [loading, setLoading] = useState(false);
  const user = JSON.parse(localStorage.getItem('eefai_user') || '{}');

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/writer/generate`, {
        template_id: 'credit_dispute_v1',
        template_version: '1.0.0',
        fields: {
          date: new Date().toISOString().split('T')[0],
          bureau_name: disputeForm.bureau,
          disputed_item: disputeForm.disputed_item,
          account_number: disputeForm.account_number,
          dispute_reason: disputeForm.dispute_reason,
          consumer_name: disputeForm.consumer_name || user.name || '',
          consumer_address: disputeForm.consumer_address
        },
        tone: 'formal',
        user_id: user.email || 'guest',
        trace_id: `dispute_${Date.now()}`
      });
      setGeneratedLetter(response.data);
    } catch (error) {
      console.error('Generation error:', error);
      alert('Failed to generate letter');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = () => {
    if (generatedLetter?.pdf_url) {
      window.open(`${API_URL}${generatedLetter.pdf_url}`, '_blank');
    }
  };

  return (
    <div className="min-h-screen bg-neutral-50 p-6">
      <div className="max-w-6xl mx-auto">
        <button onClick={() => navigate('/credit')} className="mb-4 text-primary-600 hover:text-primary-700 font-medium">
          ← Back to Credit Improvement
        </button>
        
        <h1 className="text-3xl font-bold mb-4">Credit Dispute Manager (LegalAI + WriterAgent)</h1>
        <Disclaimer page="credit" />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg p-6 border">
            <h2 className="text-xl font-semibold mb-4">Dispute Information</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">Credit Bureau</label>
                <select
                  value={disputeForm.bureau}
                  onChange={(e) => setDisputeForm({...disputeForm, bureau: e.target.value})}
                  className="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                >
                  <option value="Equifax">Equifax</option>
                  <option value="Experian">Experian</option>
                  <option value="TransUnion">TransUnion</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">Item Being Disputed</label>
                <input
                  type="text"
                  value={disputeForm.disputed_item}
                  onChange={(e) => setDisputeForm({...disputeForm, disputed_item: e.target.value})}
                  className="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  placeholder="e.g., Late payment on ABC Bank account"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">Account Number (if applicable)</label>
                <input
                  type="text"
                  value={disputeForm.account_number}
                  onChange={(e) => setDisputeForm({...disputeForm, account_number: e.target.value})}
                  className="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  placeholder="Last 4 digits"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">Reason for Dispute</label>
                <textarea
                  value={disputeForm.dispute_reason}
                  onChange={(e) => setDisputeForm({...disputeForm, dispute_reason: e.target.value})}
                  className="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  rows={4}
                  placeholder="Explain why this information is inaccurate..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">Your Name</label>
                <input
                  type="text"
                  value={disputeForm.consumer_name}
                  onChange={(e) => setDisputeForm({...disputeForm, consumer_name: e.target.value})}
                  className="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  placeholder="Full name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">Your Address</label>
                <textarea
                  value={disputeForm.consumer_address}
                  onChange={(e) => setDisputeForm({...disputeForm, consumer_address: e.target.value})}
                  className="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  rows={2}
                  placeholder="Street, City, State, ZIP"
                />
              </div>

              <button
                onClick={handleGenerate}
                disabled={loading || !disputeForm.disputed_item}
                className="w-full px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium disabled:opacity-50"
              >
                {loading ? 'Generating via WriterAgent...' : 'Generate FCRA Dispute Letter'}
              </button>
            </div>
          </div>

          <div className="bg-white rounded-lg p-6 border">
            <h2 className="text-xl font-semibold mb-4">Letter Preview</h2>
            {generatedLetter ? (
              <div>
                <div className="border rounded-lg p-4 mb-4 max-h-96 overflow-y-auto bg-neutral-50">
                  <div dangerouslySetInnerHTML={{ __html: generatedLetter.html_preview }} className="prose prose-sm max-w-none" />
                </div>
                
                <div className="space-y-3">
                  <div className="text-xs text-neutral-500 font-mono">
                    Document Hash: {generatedLetter.hash?.substring(0, 32)}...
                  </div>
                  
                  {generatedLetter.pdf_url && (
                    <button
                      onClick={handleDownloadPDF}
                      className="w-full px-6 py-3 bg-secondary-600 text-white rounded-lg hover:bg-secondary-700 font-medium"
                    >
                      ⬇️ Download PDF
                    </button>
                  )}
                  
                  <div className="p-3 bg-yellow-50 border border-yellow-200 rounded text-sm text-yellow-800">
                    ⚠️ Review carefully before sending. Send via certified mail to {disputeForm.bureau}.
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-neutral-500">
                <p>Fill out the form and click Generate to create your FCRA-compliant dispute letter.</p>
                <p className="text-xs mt-2">Powered by LegalAI + WriterAgent</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DisputeManager;
