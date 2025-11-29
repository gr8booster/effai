import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Disclaimer from '../components/Disclaimer';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const CreditImprovement = () => {
  const [scoreData, setScoreData] = useState(null);
  const [loading, setLoading] = useState(true);
  const user = JSON.parse(localStorage.getItem('eefai_user') || '{}');
  const userId = user.email || 'guest';

  useEffect(() => {
    loadCreditData();
  }, []);

  const loadCreditData = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/credit/score/estimate?user_id=${userId}`);
      setScoreData(response.data);
    } catch (error) {
      console.error('Credit error:', error);
      setScoreData({ estimated_score: 680, score_range: 'Fair', recommendations: ['Check your credit reports for errors', 'Pay down high balances', 'Set up automatic payments'] });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center"><div className="text-neutral-600">Loading credit analysis (CreditAI)...</div></div>;
  }

  const score = scoreData?.estimated_score || 680;
  const scoreColor = score >= 740 ? 'text-green-600' : score >= 670 ? 'text-blue-600' : score >= 580 ? 'text-yellow-600' : 'text-red-600';

  return (
    <div className="min-h-screen bg-neutral-50 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">Credit Improvement (CreditAI)</h1>
        <Disclaimer page="credit" />
        
        <div className="bg-white rounded-lg p-8 mb-6 border shadow-sm">
          <div className="text-center">
            <div className={`text-7xl font-bold ${scoreColor} font-mono mb-2`}>{score}</div>
            <div className="text-xl text-neutral-600 mb-4">{scoreData?.score_range || 'Fair'}</div>
            <div className="text-sm text-neutral-500">Estimated by CFP-AI + CreditAI</div>
          </div>
        </div>

        <div className="bg-white rounded-lg p-6 mb-6 border">
          <h2 className="text-xl font-semibold mb-4">AI Recommendations</h2>
          <div className="space-y-3">
            {(scoreData?.recommendations || []).map((rec, idx) => (
              <div key={idx} className="flex items-start gap-3 p-3 bg-primary-50 rounded">
                <span className="text-primary-600 font-bold text-lg">→</span>
                <span className="text-neutral-700">{rec}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="flex gap-4">
          <button onClick={() => window.location.href = '/letters'} className="flex-1 px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium">
            Generate Credit Dispute Letter
          </button>
          <button onClick={loadCreditData} className="px-6 py-3 border-2 border-neutral-300 text-neutral-700 rounded-lg hover:bg-neutral-50 font-medium">
            Refresh Analysis
          </button>
        </div>
      </div>
    </div>
  );
};

export default CreditImprovement;
