import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Disclaimer from '../components/Disclaimer';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const CreditImprovement = () => {
  const [scoreData, setScoreData] = useState(null);
  const [loading, setLoading] = useState(true);
  const user = JSON.parse(localStorage.getItem('eefai_user') || '{}');
  const userId = user.email || 'test_user_001';

  useEffect(() => {
    loadCreditData();
  }, []);

  const loadCreditData = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/credit/score/estimate?user_id=${userId}`);
      setScoreData(response.data);
    } catch (error) {
      console.error('Credit load error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-neutral-600">Loading credit analysis...</div>
      </div>
    );
  }

  const score = scoreData?.estimated_score || 650;
  const scoreColor = score >= 740 ? 'text-green-600' : score >= 670 ? 'text-blue-600' : 'text-yellow-600';

  return (
    <div className="min-h-screen bg-neutral-50 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Credit Improvement</h1>
        <Disclaimer page="credit" />
        
        {/* Score Widget */}
        <div className="bg-white rounded-lg p-8 mb-6 border shadow-sm">
          <div className="text-center">
            <div className={`text-6xl font-bold ${scoreColor} font-mono`}>{score}</div>
            <div className="text-neutral-600 mt-2">{scoreData?.score_range || 'Fair'}</div>
            <div className="mt-4 text-sm text-neutral-500">Estimated Score</div>
          </div>
        </div>

        {/* Recommendations */}
        <div className="bg-white rounded-lg p-6 mb-6 border">
          <h2 className="text-xl font-semibold mb-4">Recommendations</h2>
          <div className="space-y-3">
            {(scoreData?.recommendations || []).map((rec, idx) => (
              <div key={idx} className="flex items-start gap-3 p-3 bg-primary-50 rounded">
                <span className="text-primary-600 font-bold">•</span>
                <span className="text-neutral-700">{rec}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Action Button */}
        <button
          className="w-full px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          data-testid="generate-dispute"
        >
          Generate Dispute Letter
        </button>
      </div>
    </div>
  );
};

export default CreditImprovement;
